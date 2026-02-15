/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  The ASF licenses this file to You
 * under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.  For additional information regarding
 * copyright in this work, please see the NOTICE file in the top level
 * directory of this distribution.
 */

package org.apache.roller.weblogger.business.jpa;

import java.util.*;
import java.sql.Timestamp;
import jakarta.persistence.TypedQuery;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business.Weblogger;
import org.apache.roller.weblogger.pojos.CommentSearchCriteria;
import org.apache.roller.weblogger.pojos.WeblogEntryComment;
import org.apache.roller.weblogger.pojos.WeblogEntrySearchCriteria;
import org.apache.roller.weblogger.pojos.WeblogEntryTag;
import org.apache.roller.weblogger.pojos.WeblogEntryAttribute;
import org.apache.roller.weblogger.pojos.WeblogEntry;
import org.apache.roller.weblogger.pojos.WeblogCategory;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.pojos.User;
import org.apache.roller.weblogger.pojos.WeblogEntry.PubStatus;

// Assuming 'strategy' and 'roller' are fields of the class this block belongs to.
// Assuming 'getWeblogCategoryByName' and 'removeWeblogEntryTag' are methods of the class.
// Assuming 'LOG' is a static final field.

    /**
     * @inheritDoc
     */
    @Override
    public void removeWeblogEntry(WeblogEntry entry) throws WebloggerException {
        Weblog weblog = entry.getWebsite();
        
        CommentSearchCriteria csc = new CommentSearchCriteria();
        csc.setEntry(entry);

        // remove comments
        List<WeblogEntryComment> comments = getComments(csc);
        for (WeblogEntryComment comment : comments) {
            this.strategy.remove(comment);
        }
        
        // remove tag & tag aggregates
        if (entry.getTags() != null) {
            for (WeblogEntryTag tag : entry.getTags()) {
                removeWeblogEntryTag(tag);
            }
        }
        
        // remove attributes
        if (entry.getEntryAttributes() != null) {
            for (Iterator<WeblogEntryAttribute> it = entry.getEntryAttributes().iterator(); it.hasNext(); ) {
                WeblogEntryAttribute att = it.next();
                it.remove();
                this.strategy.remove(att);
            }
        }

        // remove entry
        this.strategy.remove(entry);
        
        // update weblog last modified date.  date updated by saveWebsite()
        if (entry.isPublished()) {
            roller.getWeblogManager().saveWeblog(weblog);
        }
        
        // remove entry from cache mapping
        this.entryAnchorToIdMap.remove(entry.getWebsite().getHandle()+":"+entry.getAnchor());
    }
    
    private List<WeblogEntry> getNextPrevEntries(WeblogEntry current, String catName,
            String locale, int maxEntries, boolean next)
            throws WebloggerException {

		if (current == null) {
			LOG.debug("current WeblogEntry cannot be null");
			return Collections.emptyList();
		}

        List<Object> params = new ArrayList<>();
        StringBuilder whereClause = new StringBuilder();

        // First parameter: website
        params.add(current.getWebsite());
        whereClause.append("e.website = ?").append(params.size());
        
        // Second parameter: status
        params.add(PubStatus.PUBLISHED);
        whereClause.append(" AND e.status = ?").append(params.size());
                
        appendPubTimeCondition(whereClause, params, current.getPubTime(), next);
        appendCategoryCondition(whereClause, params, current.getWebsite(), catName);
        appendLocaleCondition(whereClause, params, locale);
        appendOrderByClause(whereClause, next);
        
        String queryString = "SELECT e FROM WeblogEntry e WHERE " + whereClause.toString();
        TypedQuery<WeblogEntry> query = strategy.getDynamicQuery(queryString, WeblogEntry.class);
        
        setQueryParams(query, params);
        query.setMaxResults(maxEntries);
        
        return query.getResultList();
    }

    private void appendPubTimeCondition(StringBuilder whereClause, List<Object> params, Timestamp pubTime, boolean next) {
        if (next) {
            params.add(pubTime);
            whereClause.append(" AND e.pubTime > ?").append(params.size());
        } else {
            // pub time null if current article not yet published, in Draft view
            if (pubTime != null) {
                params.add(pubTime);
                whereClause.append(" AND e.pubTime < ?").append(params.size());
            }
        }
    }

    private void appendCategoryCondition(StringBuilder whereClause, List<Object> params, Weblog website, String catName) throws WebloggerException {
        if (catName != null) {
            WeblogCategory category = getWeblogCategoryByName(website, catName);
            if (category != null) {
                params.add(category);
                whereClause.append(" AND e.category = ?").append(params.size());
            } else {
                throw new WebloggerException("Cannot find category: " + catName);
            } 
        }
    }

    private void appendLocaleCondition(StringBuilder whereClause, List<Object> params, String locale) {
        if (locale != null) {
            params.add(locale + '%');
            whereClause.append(" AND e.locale like ?").append(params.size());
        }
    }

    private void appendOrderByClause(StringBuilder whereClause, boolean next) {
        if (next) {
            whereClause.append(" ORDER BY e.pubTime ASC");
        } else {
            whereClause.append(" ORDER BY e.pubTime DESC");
        }
    }

    private void setQueryParams(TypedQuery<WeblogEntry> query, List<Object> params) {
        for (int i = 0; i < params.size(); i++) {
            query.setParameter(i + 1, params.get(i));
        }
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public List<WeblogCategory> getWeblogCategories(Weblog website)
    throws WebloggerException {
        if (website == null) {
            throw new WebloggerException("website is null");
        }
        
        TypedQuery<WeblogCategory> q = strategy.getNamedQuery(
                "WeblogCategory.getByWeblog", WeblogCategory.class);
        q.setParameter(1, website);
        return q.getResultList();
    }

    /**
     * @inheritDoc
     */
    @Override
    public List<WeblogEntry> getWeblogEntries(WeblogEntrySearchCriteria wesc) throws WebloggerException {

        WeblogCategory cat = null;
        if (StringUtils.isNotEmpty(wesc.getCatName()) && wesc.getWeblog() != null) {
            cat = getWeblogCategoryByName(wesc.getWeblog(), wesc.getCatName());
        }

        List<Object> params = new ArrayList<>();
        int size = 0;
        StringBuilder queryString = new StringBuilder();
        
        if (wesc.getTags() == null || wesc.getTags().isEmpty()) {
            queryString.append("SELECT e FROM WeblogEntry e WHERE ");
        } else {
            queryString.append("SELECT e FROM WeblogEntry e JOIN e.tags t WHERE ");
            queryString.append("(");
            for (int i = 0; i < wesc.getTags().size(); i++) {
                if (i != 0
        }
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public void removeWeblogEntry(WeblogEntry entry) throws WebloggerException {
        Weblog weblog = entry.getWebsite();
        
        CommentSearchCriteria csc = new CommentSearchCriteria();
        csc.setEntry(entry);

        // remove comments
        List<WeblogEntryComment> comments = getComments(csc);
        for (WeblogEntryComment comment : comments) {
            this.strategy.remove(comment);
        }
        
        // remove tag & tag aggregates
        if (entry.getTags() != null) {
            for (WeblogEntryTag tag : entry.getTags()) {
                removeWeblogEntryTag(tag);
            }
        }
        
        // remove attributes
        if (entry.getEntryAttributes() != null) {
            for (Iterator<WeblogEntryAttribute> it = entry.getEntryAttributes().iterator(); it.hasNext();
        // but MySQL says "General error, message from server: "You can't
        // specify target table 'roller_comment' for update in FROM clause"
        
        CommentSearchCriteria csc = new CommentSearchCriteria();
this.strategy.store(entry);
        
        // update weblog last modified date.  date updated by saveWebsite()
        if(entry.isPublished()) {
            roller.getWeblogManager().saveWeblog(entry.getWebsite());
        }
        
        if(entry.isPublished()) {
            // Queue applicable pings for this update.
            roller.getAutopingManager().queueApplicableAutoPings(entry);
        }
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public void removeWeblogEntry(WeblogEntry entry) throws WebloggerException {
        // The 'weblog' variable was declared but not used in the original snippet's removeWeblogEntry.
        // Keeping it for consistency if it was intended for future use or a larger context.
        Weblog weblog = entry.getWebsite(); 
        
        removeEntryComments(entry);
        removeEntryTags(entry);
        removeEntryAttributes(entry);
    }

    private void removeEntryComments(WeblogEntry entry) throws WebloggerException {
        CommentSearchCriteria csc = new CommentSearchCriteria();
        csc.setEntry(entry);
        List<WeblogEntryComment> comments = getComments(csc);
        for (WeblogEntryComment comment : comments) {
            this.strategy.remove(comment);
        }
    }

    private void removeEntryTags(WeblogEntry entry) throws
        TypedQuery<WeblogEntry> q = strategy.getNamedQuery(
                "WeblogEntry.getByWebsite&AnchorOrderByPubTimeDesc", WeblogEntry.class);
        q.setParameter(1, website);
        q.setParameter(2, anchor);
        WeblogEntry entry;
        try {
            entry = q.getSingleResult();
        } catch (NoResultException e) {
            entry = null;
        }

        // add mapping to cache
        if (entry != null) {
            LOG.debug("entryAnchorToIdMap CACHE MISS - " + mappingKey);
            this.entryAnchorToIdMap.put(mappingKey, entry.getId());
        }
        return entry;
    }

    /**
     * @inheritDoc
     */
    @Override
    public WeblogEntry getWeblogEntryByAnchor(Weblog website,
            String anchor) throws WebloggerException {
        
        if (website == null) {
            throw new WebloggerException("Website is null");
        }
        
        if (anchor == null) {
            throw new WebloggerException("Anchor is null");
        }
        
        // mapping key is combo of weblog + anchor
        String mappingKey = website.getHandle() + ":" + anchor;
        
        // check cache first
        WeblogEntry entry = getWeblogEntryFromCache(mappingKey);
        if (entry != null) {
            return entry;
        }
        
        // cache failed, do lookup
        return getWeblogEntryFromDatabase(website, anchor, mappingKey);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public String createAnchor(WeblogEntry entry) throws WebloggerException {
        // Check for uniqueness of anchor
        String base = entry.createAnchorBase();
        String name = base;
        int count = 0;
        
        while (true) {
            if (count > 0) {
                name = base + count;
            }
            
            TypedQuery<WeblogEntry> q = strategy.getNamedQuery(
                    "WeblogEntry.getByWebsite&Anchor", WeblogEntry.class);
            q.setParameter(1, entry.getWebsite());
            q.setParameter(2, name);
            List<WeblogEntry> results = q.getResultList();
            
            if (results.isEmpty()) {
                break;
            } else {
                count++;
            }
        }
        return name;
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public boolean isDuplicateWeblogCategoryName(WeblogCategory cat)
    throws WebloggerException {
        return (getWeblogCategoryByName(
                cat.getWeblog(), cat.getName()) != null);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public boolean isWeblogCategoryInUse(WeblogCategory cat)
    throws WebloggerException {
        if (cat.getWeblog().getBloggerCategory().equals(cat)) {
            return true;
        }
        TypedQuery<WeblogEntry> q = strategy.getNamedQuery("WeblogEntry.getByCategory", WeblogEntry.class);
        q.setParameter(1, cat);
        int entryCount = q.getResultList().size();
        return entryCount > 0;
    }

    private StringBuilder appendConjuctionToWhereclause(StringBuilder whereClause, String condition) {
        if (whereClause.length() != 0) {
            whereClause.append(" AND ");
        }
        whereClause.append(condition);
        return whereClause;
    }

    private static class QueryBuilderResult {
        final StringBuilder whereClause;
        final List<Object> params;

        QueryBuilderResult(StringBuilder whereClause, List<Object> params) {
            this.whereClause = whereClause;
            this.params = params;
        }
    }

    private QueryBuilderResult buildCommentWhereClause(CommentSearchCriteria csc) {
        List<Object> params = new ArrayList<>();
        StringBuilder whereClause = new StringBuilder();
        int size = 0;

        if (csc.getEntry() != null) {
            params.add(size++, csc.getEntry());
            whereClause.append("c.weblogEntry = ?").append(size);
        } else if (csc.getWeblog() != null) {
            params.add(size++, csc.getWeblog());
            whereClause.append("c.weblogEntry.website = ?").append(size);
        }
        
        if (csc.getSearchText() != null) {
            params.add(size++, "%" + csc.getSearchText().toUpperCase() + "%");
            appendConjuctionToWhereclause(whereClause, "upper(c.content) LIKE ?").append(size);
        }
        
        if (csc.getStartDate() != null) {
            Timestamp start = new Timestamp(csc.getStartDate().getTime());
            params.add(size++, start);
            appendConjuctionToWhereclause(whereClause, "c.postTime >= ?").append(size);
        }
        
        if (csc.getEndDate() != null) {
            Timestamp end = new Timestamp(csc.getEndDate().getTime());
            params.add(size++, end);
            appendConjuctionToWhereclause(whereClause, "c.postTime <= ?").append(size);
        }
        
        if (csc.getStatus() != null) {
            params.add(size++, csc.getStatus());
            appendConjuctionToWhereclause(whereClause, "c.status = ?").append(size);
        }
        return new QueryBuilderResult(whereClause, params);
    }

    /**
     * @inheritDoc
     */
    @Override
    public List<WeblogEntryComment> getComments(CommentSearchCriteria csc) throws WebloggerException {
        
        StringBuilder queryString = new StringBuilder("SELECT c FROM WeblogEntryComment c ");
        
        QueryBuilderResult queryParts = buildCommentWhereClause(csc);
        StringBuilder whereClause = queryParts.whereClause;
        List<Object> params = queryParts.params;

        if(whereClause.length() != 0) {
            queryString.append(" WHERE ").append(whereClause);
        }
        if (csc.isReverseChrono()) {
            queryString.append(" ORDER BY c.postTime DESC");
        } else {
            queryString.append(" ORDER BY c.postTime ASC");
        }
        
        TypedQuery<WeblogEntryComment> query = strategy.getDynamicQuery(queryString.toString(), WeblogEntryComment.class);
        setFirstMax( query, csc.getOffset(), csc.getMaxResults());
        for (int i=0; i<params.size(); i++) {
            query.setParameter(i+1, params.get(i));
        }
        return query.getResultList();
        
    }
    
/**
     * @inheritDoc
     */
    @Override
    public WeblogCategory getWeblogCategory(String id)
    throws WebloggerException {
        return (WeblogCategory) this.strategy.load(
                WeblogCategory.class, id);
    }
    
    //--------------------------------------------- WeblogCategory Queries
    
    /**
     * @inheritDoc
     */
    @Override
public List<WeblogEntry> getWeblogEntriesPinnedToMain(Integer max)
    throws WebloggerException {
        TypedQuery<WeblogEntry> query = strategy.getNamedQuery(
                "WeblogEntry.getByPinnedToMain&statusOrderByPubTimeDesc", WeblogEntry.class);
        query.setParameter(1, Boolean.TRUE);
        query.setParameter(2, PubStatus.PUBLISHED);
        if (max != null) {
            query.setMaxResults(max);
        }
        return query.getResultList();
    }
    
    @Override
    public void removeWeblogEntryAttribute(String name, WeblogEntry entry)
    throws WebloggerException {
        for (Iterator<WeblogEntryAttribute> it = entry.getEntryAttributes().iterator(); it.hasNext();) {
            WeblogEntryAttribute entryAttribute = it.next();
            if (entryAttribute.getName().equals(name)) {
                //Remove it from database
                this.strategy.remove(entryAttribute);
                //Remove it from the collection
                it.remove();
            }
        }
    }
    
    private void removeWeblogEntryTag(WeblogEntryTag tag) throws WebloggerException {
        if (tag.getWeblogEntry().isPublished()) {
            updateTagCount(tag.getName(), tag.getWeblogEntry().getWebsite(), -1);
        }
        this.strategy.remove(tag);
    }

    private WeblogEntry getWeblogEntryFromCache(String mappingKey) throws WebloggerException {
        if (this.entryAnchorToIdMap.containsKey(mappingKey)) {
            WeblogEntry entry = this.getWeblogEntry(this.entryAnchorToIdMap.get(mappingKey));
            if (entry != null) {
                LOG.debug("entryAnchorToIdMap CACHE HIT - " + mappingKey);
                return entry;
            } else {
                // mapping hit with lookup miss? mapping must be old, remove it
                this.entryAnchorToIdMap.remove(mappingKey);
            }
        }
        return null; // Not found in cache or cache entry was stale
    }

    private WeblogEntry getWeblogEntryFromDatabase(Weblog website, String anchor, String mappingKey) {
        TypedQuery<WeblogEntry> q = strategy.getNamedQuery(
                "WeblogEntry.getByWebsite&AnchorOrderByPubTimeDesc", WeblogEntry.class);
        q.setParameter(1, website);
        q.setParameter(2, anchor);
        WeblogEntry entry;
        try {
            entry = q.getSingleResult();
        } catch (NoResultException e) {
            entry = null;
        }

        // add mapping to cache
        if (entry != null) {
            LOG.debug("entryAnchorToIdMap CACHE MISS - " + mappingKey);
            this.entryAnchorToIdMap.put(mappingKey, entry.getId());
        }
        return entry;
    }

    /**
     * @inheritDoc
     */
    @Override
    public WeblogEntry getWeblogEntryByAnchor(Weblog website,
            String anchor) throws WebloggerException {
        
        if (website == null) {
            throw new WebloggerException("Website is null");
        }
        
        if (anchor == null) {
            throw new WebloggerException("Anchor is null");
        }
        
        // mapping key is combo of weblog + anchor
        String mappingKey = website.getHandle() + ":" + anchor;
        
        // check cache first
        WeblogEntry entry = getWeblogEntryFromCache(mappingKey);
        if (entry != null) {
            return entry;
        }
        
        // cache failed, do lookup
        return getWeblogEntryFromDatabase(website, anchor, mappingKey);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public String createAnchor(WeblogEntry entry) throws WebloggerException {
        // Check for uniqueness of anchor
        String base = entry.createAnchorBase();
        String name = base;
        int count = 0;
        
        while (true) {
            if (count > 0) {
                name = base + count;
            }
            
            TypedQuery<WeblogEntry> q = strategy.getNamedQuery(
                    "WeblogEntry.getByWebsite&Anchor", WeblogEntry.class);
            q.setParameter(1, entry.getWebsite());
            q.setParameter(2, name);
            List<WeblogEntry> results = q.getResultList();
            
            if (results.isEmpty()) {
                break;
            } else {
                count++;
            }
        }
        return name;
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public boolean isDuplicateWeblogCategoryName(WeblogCategory cat)
    throws WebloggerException {
        return (getWeblogCategoryByName(
                cat.getWeblog(), cat.getName()) != null);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public boolean isWeblogCategoryInUse(WeblogCategory cat)
    throws WebloggerException {
        if (cat.getWeblog().getBloggerCategory().equals(cat)) {
            return true;
        }
        TypedQuery<WeblogEntry> q = strategy.getNamedQuery("WeblogEntry.getByCategory", WeblogEntry.class);
        q.setParameter(1, cat);
        int entryCount = q.getResultList().size();
        return entryCount > 0;
    }

    private StringBuilder appendConjuctionToWhereclause(StringBuilder whereClause, String condition) {
        if (whereClause.length() != 0) {
            whereClause.append(" AND ");
        }
        whereClause.append(condition);
        return whereClause;
    }

    private record QueryBuilderResult(StringBuilder whereClause, List<Object> params) {}

    private QueryBuilderResult buildCommentWhereClause(CommentSearchCriteria csc) {
        List<Object> params = new ArrayList<>();
        StringBuilder whereClause = new StringBuilder();

        if (csc.getEntry() != null) {
            params.add(csc.getEntry());
            whereClause.append("c.weblogEntry = ?").append(params.size());
        } else if (csc.getWeblog() != null) {
            params.add(csc.getWeblog());
            whereClause.append("c.weblogEntry.website = ?").append(params.size());
        }
        
        if (csc.getSearchText() != null) {
            params.add("%" + csc.getSearchText().toUpperCase() + "%");
            appendConjuctionToWhereclause(whereClause, "upper(c.content) LIKE ?").append(params.size());
        }
        
        if (csc.getStartDate() != null) {
            Timestamp start = new Timestamp(csc.getStartDate().getTime());
            params.add(start);
            appendConjuctionToWhereclause(whereClause, "c.postTime >= ?").append(params.size());
        }
        
        if (csc.getEndDate() != null) {
            Timestamp end = new Timestamp(csc.getEndDate().getTime());
            params.add(end);
            appendConjuctionToWhereclause(whereClause, "c.postTime <= ?").append(params.size());
        }
        
        if (csc.getStatus() != null) {
            params.add(csc.getStatus());
            appendConjuctionToWhereclause(whereClause, "c.status = ?").append(params.size());
        }
        return new QueryBuilderResult(whereClause, params);
    }

    /**
     * @inheritDoc
     */
    @Override
    public List<WeblogEntryComment> getComments(CommentSearchCriteria csc) throws WebloggerException {
        
        StringBuilder queryString = new StringBuilder("SELECT c
        if (expression == null || expression.trim().isEmpty()) {
            return whereClause;
        }

        if (whereClause.length() > 0) {
            whereClause.append(" AND ");
        }
        return whereClause.append(expression);
    }
    
}
/**
     * @inheritDoc
     */
    @Override
    public WeblogCategory getWeblogCategory(String id)
    throws WebloggerException {
        return (WeblogCategory) this.strategy.load(
                WeblogCategory.class, id);
    }
    
    //--------------------------------------------- WeblogCategory Queries
    
    /**
     * @inheritDoc
     */
    @Override
    public WeblogCategory getWeblogCategoryByName(Weblog weblog,
            String categoryName) throws WebloggerException {
        TypedQuery<WeblogCategory> q = strategy.getNamedQuery(
                "WeblogCategory.getByWeblog&Name", WeblogCategory.class);
        q.setParameter(1, weblog);
        q.setParameter(2, categoryName);
        try {
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    /**
     * @inheritDoc
     */
    @Override
    public WeblogEntryComment getComment(String id) throws WebloggerException {
        return (WeblogEntryComment) this.strategy.load(WeblogEntryComment.class, id);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public WeblogEntry getWeblogEntry(String id) throws WebloggerException {
        // Corrected syntax for the original short method.
        // The prompt'
private final PersistenceStrategy strategy;

    public WeblogCommentService(PersistenceStrategy strategy) {
        this.strategy = strategy;
    }

    private long executeCountQuery(String namedQuery, Object... params) throws WebloggerException {
        TypedQuery<Long> q = strategy.getNamedQuery(namedQuery, Long.class);
        for (int i = 0; i < params.length; i++) {
            // JPA parameters are 1-indexed
            q.setParameter(i + 1, params[i]);
        }
        try {
            return q.getSingleResult();
        } catch (jakarta.persistence.NoResultException | javax.persistence.NoResultException e) {
            // For count queries, a NoResultException typically means the count is 0.
            return 0L;
        } catch (jakarta.persistence.PersistenceException | javax.persistence.PersistenceException e) {
            throw new WebloggerException("Error executing count query: " + namedQuery, e);
        }
    }

    public long getCommentCount() throws WebloggerException {
        return executeCountQuery("WeblogEntryComment.getCountAllDistinctByStatus", ApprovalStatus.APPROVED);
    }

    public long getCommentCount(Weblog website) throws WebloggerException {
        return executeCountQuery("WeblogEntryComment.getCountDistinctByWebsite&Status", website, ApprovalStatus.APPROVED);
    }

    public static StringBuilder appendConjunctionToWhereclause(StringBuilder whereClause,
            String expression) {
        if (expression == null || expression.trim().isEmpty()) {
            return whereClause;
        }

        if (whereClause.length() > 0) {
            whereClause.append(" AND ");
        }
        return whereClause.append(expression);
    }
}
return whereClause;
        }

        appendAndSeparator(whereClause);
        return whereClause.append(expression);
    }
    
    private void appendAndSeparator(StringBuilder builder) {
        if (builder.length() > 0) {
            builder.append(" AND ");
        }
    }
}