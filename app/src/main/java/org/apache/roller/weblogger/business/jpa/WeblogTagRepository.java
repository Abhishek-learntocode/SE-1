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
import java.util.Date;
import jakarta.persistence.NoResultException;
import jakarta.persistence.Query;
import jakarta.persistence.TypedQuery;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.pojos.WeblogEntryTag;
import org.apache.roller.weblogger.pojos.WeblogEntryTagAggregate;


/**
 * Repository for tag aggregate persistence operations.
 *
 * Extracted from JPAWeblogEntryManagerImpl to resolve Feature Envy smell:
 * the updateTagCount() and removeWeblogEntryTag() methods were more interested
 * in JPAPersistenceStrategy members than in their own class's state.
 *
 * This class encapsulates tag aggregate count management — incrementing,
 * decrementing, creating, and cleaning up WeblogEntryTagAggregate rows.
 */
@com.google.inject.Singleton
public class WeblogTagRepository {

    private static final Log LOG = LogFactory.getLog(WeblogTagRepository.class);

    private final JPAPersistenceStrategy strategy;

    @com.google.inject.Inject
    protected WeblogTagRepository(JPAPersistenceStrategy strategy) {
        LOG.debug("Instantiating WeblogTagRepository");
        this.strategy = strategy;
    }

    /**
     * This method maintains the tag aggregate table up-to-date with total counts. More
     * specifically every time this method is called it will act upon exactly two rows
     * in the database (tag,website,count), one with website matching the argument passed
     * and one where website is null. If the count ever reaches zero, the row must be deleted.
     *
     * @param name      The tag name
     * @param website   The website to used when updating the stats.
     * @param amount    The amount to increment the tag count (it can be positive or negative).
     * @throws WebloggerException
     */
    public void updateTagCount(String name, Weblog website, int amount)
    throws WebloggerException {
        if (amount == 0) {
            throw new WebloggerException("Tag increment amount cannot be zero.");
        }
        
        if (website == null) {
            throw new WebloggerException("Website cannot be NULL.");
        }
        
        // The reason why add order lastUsed desc is to make sure we keep picking the most recent
        // one in the case where we have multiple rows (clustered environment)
        // eventually that second entry will have a very low total (most likely 1) and
        // won't matter
        TypedQuery<WeblogEntryTagAggregate> weblogQuery = strategy.getNamedQuery(
                "WeblogEntryTagAggregate.getByName&WebsiteOrderByLastUsedDesc", WeblogEntryTagAggregate.class);
        weblogQuery.setParameter(1, name);
        weblogQuery.setParameter(2, website);
        WeblogEntryTagAggregate weblogTagData;
        try {
            weblogTagData = weblogQuery.getSingleResult();
        } catch (NoResultException e) {
            weblogTagData = null;
        }

        TypedQuery<WeblogEntryTagAggregate> siteQuery = strategy.getNamedQuery(
                "WeblogEntryTagAggregate.getByName&WebsiteNullOrderByLastUsedDesc", WeblogEntryTagAggregate.class);
        siteQuery.setParameter(1, name);
        WeblogEntryTagAggregate siteTagData;
        try {
            siteTagData = siteQuery.getSingleResult();
        } catch (NoResultException e) {
            siteTagData = null;
        }
        Timestamp lastUsed = new Timestamp((new Date()).getTime());
        
        // create it only if we are going to need it.
        if (weblogTagData == null && amount > 0) {
            weblogTagData = new WeblogEntryTagAggregate(null, website, name, amount);
            weblogTagData.setLastUsed(lastUsed);
            strategy.store(weblogTagData);
            
        } else if (weblogTagData != null) {
            weblogTagData.setTotal(weblogTagData.getTotal() + amount);
            weblogTagData.setLastUsed(lastUsed);
            strategy.store(weblogTagData);
        }
        
        // create it only if we are going to need it.
        if (siteTagData == null && amount > 0) {
            siteTagData = new WeblogEntryTagAggregate(null, null, name, amount);
            siteTagData.setLastUsed(lastUsed);
            strategy.store(siteTagData);
            
        } else if (siteTagData != null) {
            siteTagData.setTotal(siteTagData.getTotal() + amount);
            siteTagData.setLastUsed(lastUsed);
            strategy.store(siteTagData);
        }
        
        // delete all bad counts
        Query removeq = strategy.getNamedUpdate(
                "WeblogEntryTagAggregate.removeByTotalLessEqual");
        removeq.setParameter(1, 0);
        removeq.executeUpdate();
    }

    /**
     * Removes a single WeblogEntryTag, decrementing the associated tag aggregate
     * count if the owning entry is published.
     *
     * @param tag The tag to remove
     * @throws WebloggerException
     */
    public void removeWeblogEntryTag(WeblogEntryTag tag) throws WebloggerException {
        if (tag.getWeblogEntry().isPublished()) {
            updateTagCount(tag.getName(), tag.getWeblogEntry().getWebsite(), -1);
        }
        this.strategy.remove(tag);
    }
}
