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

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.Iterator;
import java.util.List;
import jakarta.persistence.TypedQuery;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business
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
        csc.setWeblog(weblog);
        csc.setEntry(entry);
        csc.setSearchText(searchString);
        csc.setStartDate(startDate);
        csc.setEndDate(endDate);
        csc.setStatus(status);

        List<WeblogEntryComment> comments = getComments(csc);
        int count = 0;
        for (WeblogEntryComment comment : comments) {
            removeComment(comment);
            count++;
        }
        return count;
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
        return (WeblogEntry)strategy.load(WeblogEntry.class, id);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public Map<Date, List<WeblogEntry>> getWeblogEntryObjectMap(WeblogEntrySearchCriteria wesc) throws WebloggerException {
        TreeMap<Date, List<WeblogEntry>> map = new TreeMap<>(Collections.reverseOrder());

        List<WeblogEntry> entries = getWeblogEntries(wesc);

        Calendar cal = Calendar.getInstance();
        if (wesc.getWeblog() != null) {
            cal.setTimeZone(wesc.getWeblog().getTimeZoneInstance());
        }

        for (WeblogEntry entry : entries) {
            Date sDate = DateUtil.getNoonOfDay(entry.getPubTime(), cal);
            List<WeblogEntry> dayEntries = map.computeIfAbsent(sDate, k -> new ArrayList<>());
            dayEntries.add(entry);
        }
        return map;
    }

    /**
     * @inheritDoc
     */
    @Override
    public Map<Date, String> getWeblogEntryStringMap(WeblogEntrySearchCriteria wesc) throws WebloggerException {
        TreeMap<Date, String> map = new TreeMap<>(Collections.reverseOrder());

        List<WeblogEntry> entries = getWeblogEntries(wesc);

        Calendar cal = Calendar.getInstance();
        SimpleDateFormat formatter = DateUtil.get8charDateFormat();
        if (wesc.getWeblog() != null) {
            TimeZone tz = wesc.getWeblog().getTimeZoneInstance();
            cal.setTimeZone(tz);
            formatter.setTimeZone(tz);
        }

        for (WeblogEntry entry : entries) {
            Date sDate = DateUtil.getNoonOfDay(entry.getPubTime(), cal);
            if (map.get(sDate) == null) {
                map.put(sDate, formatter.format(sDate));
            }
        }
        return map;
    }

    /**
     * @inheritDoc
     */
    @Override
    public List<StatCount> getMostCommentedWeblogEntries(Weblog website,
            Date startDate, Date endDate, int offset,
            int length) throws WebloggerException {
        TypedQuery<WeblogEntryComment> query;
        List<WeblogEntryComment> queryResults;

        Timestamp end = new Timestamp(endDate != null? endDate.getTime() : new Date().getTime());

        if (website != null) {
            if (startDate != null) {
                Timestamp start = new Timestamp(startDate.getTime());
                query = strategy.getNamedQuery(
                        "WeblogEntryComment.getMostCommentedWeblogEntryByWebsite&EndDate&StartDate",
                        WeblogEntryComment.class);
                query.setParameter(1, website);
                query.setParameter(2, end);
                query.setParameter(3, start);
            } else {
                query = strategy.getNamedQuery(
                        "WeblogEntryComment.getMostCommentedWeblogEntryByWebsite&EndDate", WeblogEntryComment.class);
                query.setParameter(1, website);
                query.setParameter(2, end);
            }
        } else {
            if (startDate != null) {
                Timestamp start = new Timestamp(startDate.getTime());
                query = strategy.getNamedQuery(
                        "WeblogEntryComment.getMostCommentedWeblogEntryByEndDate&StartDate", WeblogEntryComment.class);
                query.setParameter(1, end);
                query.setParameter(2, start);
            } else {
                query = strategy.getNamedQuery(
                        "WeblogEntryComment.getMostCommentedWeblogEntryByEndDate", WeblogEntryComment.class);
                query.setParameter(1, end);
            }
        }
        setFirstMax( query, offset, length);
        queryResults = query.getResultList();
        List<StatCount> results = new ArrayList<>();
        if (queryResults != null) {
            for (Object obj : queryResults) {
                Object[] row = (Object[]) obj;
                StatCount sc = new StatCount(
                        (String)row[1],                             // weblog handle
                        (String)row[2],                             // entry anchor
                        (String)row[3],                             // entry title
                        "statCount.weblogEntryCommentCountType",    // stat desc
                        ((Long)row[0]));                            // count
                sc.setWeblogHandle((String)row[1]);
                results.add(sc);
            }
        }
        // Original query ordered by desc count.
        // JPA QL doesn't allow queries to be ordered by agregates; do it in memory
        results.sort(STAT_COUNT_COUNT_REVERSE_COMPARATOR);
        
        return results;
    }
    
    /**
     * @inheritDoc
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
        Weblog weblog = entry.getWebsite();
        
        CommentSearchCriteria csc = new CommentSearchCriteria();
        csc.setEntry(entry);

        // remove comments associated with this entry
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
            for (Iterator<WeblogEntryAttribute> it = entry.getEntryAttributes().iterator(); it
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
        return (WeblogEntry)strategy.load(WeblogEntry.class,
    /**
     * @inheritDoc
     */
    @Override
    public long getEntryCount() throws WebloggerException {
        TypedQuery<Long> q = strategy.getNamedQuery(
                "WeblogEntry.getCountDistinctByStatus", Long.class);
        q.setParameter(1, PubStatus.PUBLISHED);
        return q.getResultList().get(0);
    }
    
    /**
     * @inheritDoc
     */
    @Override
    public long getEntryCount(Weblog website) throws WebloggerException {
        TypedQuery<Long> q = strategy.getNamedQuery(
                "WeblogEntry.getCountDistinctByStatus&Website", Long.class);
        q.setParameter(1, PubStatus.PUBLISHED);
        q.setParameter(2, website);
        return q.getResultList().get(0);
    }

    /**
     * Appends given expression to given whereClause. If whereClause already
     * has other conditions, an " AND " is also appended before appending
     * the expression
     * @param whereClause The given where Clauuse
     * @param expression The given expression
     * @return the whereClause.
     */
    private static StringBuilder appendConjuctionToWhereclause(StringBuilder whereClause,
            String expression) {
        if (whereClause.length() != 0 && expression.length() != 0) {
            whereClause.append(" AND ");
        }
        return whereClause.append(expression);
    }
    
}

}
        setFirstMax( query, offset, limit);
        queryResults = query.getResultList();
        
        double min = Integer.MAX_VALUE;
        double max = Integer.MIN_VALUE;
        
        List<TagStat> results = new ArrayList<>(limit >= 0 ? limit : 25);
        
        if (queryResults != null) {
            for (Object obj : queryResults) {
                Object[] row = (Object[]) obj;
                TagStat t = new TagStat();
                t.setName((String) row[0]);
                t.setCount(((Number) row[1]).intValue());

                min = Math.min(min, t.getCount());
                max = Math.max(max, t.getCount());
                results.add(t);
            }
        }

        min = Math.log(1+min);
        max = Math.log(1+max);
        
        double range = Math.max(.01, max - min) * 1.0001;
        
        for (TagStat t : results) {
            t.setIntensity((int) (1 + Math.floor(5 * (Math.log(1+t.getCount()) - min) / range)));
        }

        // sort results by name, because query had to sort by total
        results.sort(TAG_STAT_NAME_COMPARATOR);
interface PersistenceStrategy {
    <T> TypedQuery<T> getNamedQuery(String queryName, Class<T> resultClass);
    Query getNamedUpdate(String queryName);
    void store(Object entity);
    void remove(Object entity);
}

class Weblog { /* ... */ }
class WeblogHitCount {
    private Weblog weblog;
    private int dailyHits;

    public Weblog getWeblog() { return weblog; }
    public void setWeblog(Weblog weblog) { this.weblog = weblog; }
    public int getDailyHits() { return dailyHits; }
    public void setDailyHits(int dailyHits) { this.dailyHits = dailyHits; }
}
class WebloggerException extends Exception {
    public WebloggerException(String message) { super(message); }
}
enum ApprovalStatus { APPROVED, PENDING, REJECTED }
enum PubStatus { PUBLISHED, DRAFT, PENDING }

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import javax.persistence.NoResultException;
import javax.persistence.Query;
import javax.persistence.TypedQuery;

public class WeblogHitCountService {

    private final PersistenceStrategy strategy;

    public WeblogHitCountService(PersistenceStrategy strategy) {
        this.strategy = strategy;
    }

    public WeblogHitCount getHitCountByWeblog(Weblog weblog) throws WebloggerException {
        TypedQuery<WeblogHitCount> q = strategy.getNamedQuery("WeblogHitCount.getByWeblog", WeblogHitCount.class);
        q.setParameter(1, weblog);
        try {
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    public List<WeblogHitCount> getHotWeblogs(int sinceDays, int offset, int length) throws WebloggerException {
        Date startDate = getStartDateNow(sinceDays);

        TypedQuery<WeblogHitCount> query;
        query = strategy.getNamedQuery(
                "WeblogHitCount.getByWeblogEnabledTrueAndActiveTrue&DailyHitsGreaterThenZero&WeblogLastModifiedGreaterOrderByDailyHitsDesc",
                WeblogHitCount.class);
        query.setParameter(1, startDate);
        setFirstMax(query, offset, length);
        return query.getResultList();
    }

    private void setFirstMax(Query query, int offset, int length) {
        if (offset != 0) {
            query.setFirstResult(offset);
        }
        if (length != -1) {
            query.setMaxResults(length);
        }
    }

    private Date getStartDateNow(int sinceDays) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(new Date());
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

        // seems silly, why is this not done in WeblogEntry?

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
        // Use a COUNT query for efficiency instead of fetching all results and checking size
        TypedQuery<Long> q = strategy.getNamedQuery("WeblogEntry.countByCategory", Long.class);
        q.setParameter(1, cat);
        Long entryCount = q.getSingleResult();
        return entryCount > 0;
    }

    private void appendCondition(StringBuilder whereClause, String condition) {
        if (whereClause.length() != 0) {
            whereClause.append(" AND ");
        }
        whereClause.append(condition);
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
        int paramIndex = 0; // Use a dedicated index for positional parameters

        if (csc.getEntry() != null) {
            params.add(csc.getEntry());
            appendCondition(whereClause, "c.weblogEntry = ?" + (++paramIndex));
        } else if (csc.getWeblog() != null) {
            params.add(csc.getWeblog());
            appendCondition(whereClause, "c.weblogEntry.website = ?" + (++paramIndex));
        }
        
        if (csc.getSearchText() != null) {
            params.add("%" + csc.getSearchText().toUpperCase() + "%");
            appendCondition(whereClause, "upper(c.content) LIKE ?" + (++paramIndex));
        }
        
        if (csc.getStartDate() != null) {
            Timestamp start = new Timestamp(csc.getStartDate().getTime());
            params.add(start);
            appendCondition(whereClause, "c.postTime >= ?" + (++paramIndex));
        }
        
        if (csc.getEndDate() != null) {
            Timestamp end = new Timestamp(csc.getEndDate().getTime());
            params.add(end);
            appendCondition(whereClause, "c.postTime <= ?" + (++paramIndex));
        }
        
        if (csc.getStatus() != null) {
            params.add(csc.getStatus());
            appendCondition(whereClause, "c.status = ?" + (++paramIndex));
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
    
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Comparator;
import java.util.Date;
import java.util.List;
import javax.persistence.NoResultException;
import javax.persistence.Query;
import javax.persistence.TypedQuery;

interface PersistenceStrategy {
    <T> TypedQuery<T> getNamedQuery(String queryName, Class<T> resultClass);
    Query getNamedUpdate(String queryName);
    void store(Object entity);
    void remove(Object entity);
    Object load(Class<?> entityClass, String id); // Added for WeblogEntryService methods
}

class Weblog { /* ... */ }

class WeblogHitCount {
    private Weblog weblog;
    private int dailyHits;

    public Weblog getWeblog() { return weblog; }
    public void setWeblog(Weblog weblog) { this.weblog = weblog; }
    public int getDailyHits() { return dailyHits; }
    public void setDailyHits(int dailyHits) { this.dailyHits = dailyHits; }
}

class WebloggerException extends Exception {
    public WebloggerException(String message) { super(message); }
}

enum ApprovalStatus { APPROVED, PENDING, REJECTED }
enum PubStatus { PUBLISHED, DRAFT, PENDING }

class TagStat {
    private String name;
    private int count;
    private int intensity;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getCount() { return count; }
    public void setCount(int count) { this.count = count; }
    public int getIntensity() { return intensity; }
    public void setIntensity(int intensity) { this.intensity = intensity; }
}

class WeblogCategory { /* ... */ }
class WeblogEntryComment { /* ... */ }
class WeblogEntry { /* ... */ }

public class WeblogEntryService { // Assuming this class contains the initial methods
    private final PersistenceStrategy strategy;

    public WeblogEntryService(PersistenceStrategy strategy) {
        this.strategy = strategy;
    }

    private static final Comparator<TagStat> TAG_STAT_NAME_COMPARATOR =
            Comparator.comparing(TagStat::getName);

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
        TypedQuery<WeblogCategory> q = strategy.
private final PersistenceStrategy strategy;

    public WeblogCommentService(PersistenceStrategy strategy) {
        this.strategy = strategy;
    }

    private long getCommentCountInternal(String queryName, Object... params) throws WebloggerException {
        TypedQuery<Long> q = strategy.getNamedQuery(queryName, Long.class);
        for (int i = 0; i < params.length; i++) {
            q.setParameter(i + 1, params[i]);
        }
        return q.getResultList().get(0);
    }

    public long getCommentCount() throws WebloggerException {
        return getCommentCountInternal("WeblogEntryComment.getCountAllDistinctByStatus", ApprovalStatus.APPROVED);
    }

    public long getCommentCount(Weblog website) throws WebloggerException {
        return getCommentCountInternal("WeblogEntryComment.getCountDistinctByWebsite&Status", website, ApprovalStatus.APPROVED);
    }
}
return whereClause;
        }
        return appendExpressionToClause(whereClause, expression);
    }

    private StringBuilder appendExpressionToClause(StringBuilder whereClause, String expression) {
        if (whereClause.length() > 0) {
            whereClause.append(" AND ");
        }
        return whereClause.append(expression);
    }
    
}