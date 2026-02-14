/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  The ASF licenses this file to You
 * under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.  For additional information regarding
 * copyright in this work, please see the NOTICE file in the top level
 * directory of this distribution.
 */

package org.apache.roller.weblogger.pojos.wrapper;

import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TimeZone;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.text.StringEscapeUtils;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business.BookmarkManager;
import org.apache.roller.weblogger.business.URLStrategy;
import org.apache.roller.weblogger.business.Weblogger;
import org.apache.roller.weblogger.business.WebloggerFactory;
import org.apache.roller.weblogger.business.WeblogEntryManager;
import org.apache.roller.weblogger.business.plugins.PluginManager;
import org.apache.roller.weblogger.business.plugins.entry.WeblogEntryPlugin;
import org.apache.roller.weblogger.business.themes.ThemeManager;
import org.apache.roller.weblogger.pojos.CommentSearchCriteria;
import org.apache.roller.weblogger.pojos.TagStat;
import org.apache.roller.weblogger.pojos.WeblogEntry;
import org.apache.roller.weblogger.pojos.WeblogEntry.PubStatus;
import org.apache.roller.weblogger.pojos.WeblogEntryComment;
import org.apache.roller.weblogger.pojos.WeblogEntrySearchCriteria;
import org.apache.roller.weblogger.pojos.WeblogHitCount;
import org.apache.roller.weblogger.pojos.WeblogTheme;
import org.apache.roller.weblogger.util.HTMLSanitizer;

import java.util.stream.Collectors;
import org.apache.roller.weblogger.pojos.ThemeTemplate.ComponentType;
import org.apache.roller.weblogger.pojos.Weblog;


/**
 * Pojo safety wrapper for Weblog objects.
 */
public final class WeblogWrapper {
    
    private static final Log log = LogFactory.getLog(WeblogWrapper.class);

    private static final int MAX_ENTRIES = 100;

    // keep a reference to the wrapped pojo
    private final Weblog pojo;
    
    // url strategy to use for any url building
    private final URLStrategy urlStrategy;

    // this is private so that we can force the use of the .wrap(pojo) method
    private WeblogWrapper(Weblog toWrap, URLStrategy strat) {
        this.pojo = toWrap;
        this.urlStrategy = strat;
    }
    
    
    // wrap the given pojo if it is not null with detected type
    public static WeblogWrapper wrap(Weblog toWrap, URLStrategy strat) {
        if (toWrap != null) {
            return new WeblogWrapper(toWrap, strat);
        }
        return null;
    }


    public ThemeTemplateWrapper getTemplateByAction(ComponentType action) throws WebloggerException {
        WeblogTheme theme = getThemeSafe();
        return theme != null ? ThemeTemplateWrapper.wrap(theme.getTemplateByAction(action)) : null;
    }
    
    
    public ThemeTemplateWrapper getTemplateByName(String name) throws WebloggerException {
        WeblogTheme theme = getThemeSafe();
        return theme != null ? ThemeTemplateWrapper.wrap(theme.getTemplateByName(name)) : null;
    }
    
    
    public ThemeTemplateWrapper getTemplateByLink(String link) throws WebloggerException {
        WeblogTheme theme = getThemeSafe();
        return theme != null ? ThemeTemplateWrapper.wrap(theme.getTemplateByLink(link)) : null;
    }
    
    
    public List<ThemeTemplateWrapper> getTemplates() throws WebloggerException {
        WeblogTheme theme = getThemeSafe();
        if (theme == null) {
            return Collections.emptyList();
        }
        return theme.getTemplates().stream()
                .map(ThemeTemplateWrapper::wrap)
                .collect(Collectors.toList());
    }
    
    
    public String getId() {
        return this.pojo.getId();
    }
    
    
    public String getHandle() {
        return this.pojo.getHandle();
    }
    
    
    public String getName() {
        return StringEscapeUtils.escapeHtml4(this.pojo.getName());
    }
    
    public String getTagline() {
        return HTMLSanitizer.conditionallySanitize(this.pojo.getTagline());
    }

    public UserWrapper getCreator() {
        try {
            return UserWrapper.wrap(
                WebloggerFactory.getWeblogger().getUserManager()
                    .getUserByUserName(this.pojo.getCreatorUserName()));
        } catch (Exception e) {
            log.error("ERROR fetching user object for username: " + this.pojo.getCreatorUserName(), e);
        }
        return null;
    }
    
    public Boolean getEnableBloggerApi() {
        return this.pojo.getEnableBloggerApi();
    }

    public WeblogCategoryWrapper getBloggerCategory() {
        return WeblogCategoryWrapper.wrap(this.pojo.getBloggerCategory(), urlStrategy);
    }
    
    public String getEditorPage() {
        return this.pojo.getEditorPage();
    }

    public String getBannedwordslist() {
        return this.pojo.getBannedwordslist();
    }
    
    
    public Boolean getAllowComments() {
        return this.pojo.getAllowComments();
    }
    
    
    public Boolean getDefaultAllowComments() {
        return this.pojo.getDefaultAllowComments();
    }
    
    
    public int getDefaultCommentDays() {
        return this.pojo.getDefaultCommentDays();
    }
    
    
    public Boolean getModerateComments() {
        return this.pojo.getModerateComments();
    }

    public String getAnalyticsCode() {
        return HTMLSanitizer.conditionallySanitize(this.pojo.getAnalyticsCode());
    }

    public Boolean getEmailComments() {
        return this.pojo.getEmailComments();
    }

    public String getEmailAddress() {
        return this.pojo.getEmailAddress();
    }
    
    
    public String getEditorTheme() {
        return this.pojo.getEditorTheme();
    }
    
    
    public String getLocale() {
        return this.pojo.getLocale();
    }
    
    
    public String getTimeZone() {
        return this.pojo.getTimeZone();
    }
    
    
    public Date getDateCreated() {
        return this.pojo.getDateCreated();
    }


    public String getDefaultPlugins() {
        return this.pojo.getDefaultPlugins();
    }

    public Locale getLocaleInstance() {
        return this.pojo.getLocaleInstance();
    }
    
    
    public TimeZone getTimeZoneInstance() {
        return this.pojo.getTimeZoneInstance();
    }
    
    
    public int getEntryDisplayCount() {
        return this.pojo.getEntryDisplayCount();
    }
    
    
    public Boolean getVisible() {
        return this.pojo.getVisible();
    }

    /* deprecated in Roller 5.1 */
    @Deprecated
    public Boolean getEnabled() {
        return getVisible();
    }

    public Boolean getActive() {
        return this.pojo.getActive();
    }
    
    
    public Date getLastModified() {
        return this.pojo.getLastModified();
    }
    
    
    public boolean isEnableMultiLang() {
        return this.pojo.isEnableMultiLang();
    }
    
    
    public boolean isShowAllLangs() {
        return this.pojo.isShowAllLangs();
    }
    
    
    public String getStylesheet() throws WebloggerException {
        // custom stylesheet comes from the weblog theme
        WeblogTheme theme = getThemeSafe();
        if(theme != null && theme.getStylesheet() != null) {
            return urlStrategy.getWeblogPageURL(this.pojo, null, theme.getStylesheet().getLink(), null, null, null, null, 0, false);
        }
        return null;
    }

    
    /**
     * Get path to weblog icon image if defined.
     *
     * This method is somewhat smart in the sense that it will check the entered
     * icon value and if it is a full url then it will be left alone, but if it
     * is a relative path to a file in the weblog's uploads section then it will
     * build the full url to that resource and return it.
     */
    public String getIcon() {
        
        String iconPath = this.pojo.getIconPath();
        if(iconPath == null) {
            return null;
        }
        
        if(iconPath.startsWith("http") || iconPath.startsWith("/")) {
            // if icon path is a relative path then assume it's a weblog resource
            return iconPath;
        } else {
            // otherwise it's just a plain old url
            return urlStrategy.getWeblogResourceURL(this.pojo, iconPath, false);
        }
        
    }
    
    
    public String getAbout() {
        return HTMLSanitizer.conditionallySanitize(this.pojo.getAbout());
    }
    
    
    
    public String getURL() {
        return urlStrategy.getWeblogURL(this.pojo, null, false);
    }
    
    
    public String getAbsoluteURL() {
        return urlStrategy.getWeblogURL(this.pojo, null, true);
    }
    
    
    public WeblogEntryWrapper getWeblogEntry(String anchor) {
        WeblogEntry entry = null;
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager wmgr = roller.getWeblogEntryManager();
            entry = wmgr.getWeblogEntryByAnchor(this.pojo, anchor);
        } catch (WebloggerException e) {
            log.error("ERROR: getting entry by anchor");
        }
        return WeblogEntryWrapper.wrap(entry, urlStrategy);
    }


    public List<WeblogCategoryWrapper> getWeblogCategories() {
        return this.pojo.getWeblogCategories().stream()
                .map(cat -> WeblogCategoryWrapper.wrap(cat, urlStrategy))
                .collect(Collectors.toList());
    }

    public WeblogCategoryWrapper getWeblogCategory(String categoryName) {
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager wmgr = roller.getWeblogEntryManager();
            if (categoryName != null && !categoryName.equals("nil")) {
                return WeblogCategoryWrapper.wrap(
                    wmgr.getWeblogCategoryByName(this.pojo, categoryName), urlStrategy);
            } else {
                return WeblogCategoryWrapper.wrap(
                    this.pojo.getWeblogCategories().iterator().next(), urlStrategy);
            }
        } catch (WebloggerException e) {
            log.error("ERROR: fetching category: " + categoryName, e);
        }
        return null;
    }

    
    public List<WeblogEntryWrapper> getRecentWeblogEntries(String cat, int length) {
        if (cat != null && "nil".equals(cat)) {
            cat = null;
        }
        if (length > MAX_ENTRIES) {
            length = MAX_ENTRIES;
        }
        if (length < 1) {
            return Collections.emptyList();
        }
        try {
            WeblogEntryManager wmgr = WebloggerFactory.getWeblogger().getWeblogEntryManager();
            WeblogEntrySearchCriteria wesc = new WeblogEntrySearchCriteria();
            wesc.setWeblog(this.pojo);
            wesc.setCatName(cat);
            wesc.setStatus(PubStatus.PUBLISHED);
            wesc.setMaxResults(length);
            return wmgr.getWeblogEntries(wesc).stream()
                    .map(entry -> WeblogEntryWrapper.wrap(entry, urlStrategy))
                    .collect(Collectors.toList());
        } catch (WebloggerException e) {
            log.error("ERROR: getting recent entries", e);
        }
        return Collections.emptyList();
    }
    
    
    public List<WeblogEntryWrapper> getRecentWeblogEntriesByTag(String tag, int length) {
        if (tag != null && "nil".equals(tag)) {
            tag = null;
        }
        if (length > MAX_ENTRIES) {
            length = MAX_ENTRIES;
        }
        if (length < 1) {
            return Collections.emptyList();
        }
        List<String> tags = Collections.emptyList();
        if (tag != null) {
            tags = List.of(tag);
        }
        try {
            WeblogEntryManager wmgr = WebloggerFactory.getWeblogger().getWeblogEntryManager();
            WeblogEntrySearchCriteria wesc = new WeblogEntrySearchCriteria();
            wesc.setWeblog(this.pojo);
            wesc.setTags(tags);
            wesc.setStatus(PubStatus.PUBLISHED);
            wesc.setMaxResults(length);
            return wmgr.getWeblogEntries(wesc).stream()
                    .map(entry -> WeblogEntryWrapper.wrap(entry, urlStrategy))
                    .collect(Collectors.toList());
        } catch (WebloggerException e) {
            log.error("ERROR: getting recent entries", e);
        }
        return Collections.emptyList();
    }
    
    
    public List<WeblogEntryCommentWrapper> getRecentComments(int length) {
        if (length > MAX_ENTRIES) {
            length = MAX_ENTRIES;
        }
        if (length < 1) {
            return Collections.emptyList();
        }
        try {
            WeblogEntryManager wmgr = WebloggerFactory.getWeblogger().getWeblogEntryManager();
            CommentSearchCriteria csc = new CommentSearchCriteria();
            csc.setWeblog(this.pojo);
            csc.setStatus(WeblogEntryComment.ApprovalStatus.APPROVED);
            csc.setReverseChrono(true);
            csc.setMaxResults(length);
            return wmgr.getComments(csc).stream()
                    .map(wec -> WeblogEntryCommentWrapper.wrap(wec, urlStrategy))
                    .collect(Collectors.toList());
        } catch (WebloggerException e) {
            log.error("ERROR: getting recent comments", e);
        }
        return Collections.emptyList();
    }
    
    
    public WeblogBookmarkFolderWrapper getBookmarkFolder(String folderName) {
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            BookmarkManager bmgr = roller.getBookmarkManager();
            if (folderName == null || folderName.equals("nil") || folderName.trim().equals("/")) {
                return WeblogBookmarkFolderWrapper.wrap(bmgr.getDefaultFolder(this.pojo));
            } else {
                return WeblogBookmarkFolderWrapper.wrap(bmgr.getFolder(this.pojo, folderName));
            }
        } catch (WebloggerException re) {
            log.error("ERROR: fetching folder for weblog", re);
        }
        return null;
    }

    public int getTodaysHits() {
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager mgr = roller.getWeblogEntryManager();
            WeblogHitCount hitCount = mgr.getHitCountByWeblog(this.pojo);
            return (hitCount != null) ? hitCount.getDailyHits() : 0;
        } catch (WebloggerException e) {
            log.error("Error getting weblog hit count", e);
        }
        return 0;
    }
    
    public List<TagStat> getPopularTags(int sinceDays, int length) {
        Date startDate = null;
        if (sinceDays > 0) {
            Calendar cal = Calendar.getInstance();
            cal.setTime(new Date());
            cal.add(Calendar.DATE, -1 * sinceDays);
            startDate = cal.getTime();
        }
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager wmgr = roller.getWeblogEntryManager();
            return wmgr.getPopularTags(this.pojo, startDate, 0, length);
        } catch (Exception e) {
            log.error("ERROR: fetching popular tags for weblog " + this.pojo.getName(), e);
        }
        return Collections.emptyList();
    }
    
    
    public long getCommentCount() {
        long count = 0;
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager mgr = roller.getWeblogEntryManager();
            count = mgr.getCommentCount(this.pojo);
        } catch (WebloggerException e) {
            log.error("Error getting comment count for weblog " + this.pojo.getName(), e);
        }
        return count;
    }
    
    
    public long getEntryCount() {
        long count = 0;
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            WeblogEntryManager mgr = roller.getWeblogEntryManager();
            count = mgr.getEntryCount(this.pojo);
        } catch (WebloggerException e) {
            log.error("Error getting entry count for weblog " + this.pojo.getName(), e);
        }
        return count;
    }

    /**
     * Get initialized plugins for use during rendering process.
     */
    public Map<String, WeblogEntryPlugin> getInitializedPlugins() {
        try {
            Weblogger roller = WebloggerFactory.getWeblogger();
            PluginManager ppmgr = roller.getPluginManager();
            return ppmgr.getWeblogEntryPlugins(this.pojo);
        } catch (Exception e) {
            log.error("ERROR: initializing plugins");
        }
        return null;
    }
    
    
    /**
     * Safely retrieve the WeblogTheme for this weblog by delegating to ThemeManager.
     * Returns null if theme cannot be loaded.
     */
    private WeblogTheme getThemeSafe() {
        try {
            ThemeManager themeMgr = WebloggerFactory.getWeblogger().getThemeManager();
            return themeMgr.getTheme(this.pojo);
        } catch (WebloggerException ex) {
            log.error("Error getting theme for weblog - " + this.pojo.getHandle(), ex);
        }
        return null;
    }

    /**
     * this is a special method to access the original pojo
     * we don't really want to do this, but it's necessary
     * because some parts of the rendering process still need the
     * original pojo object
     */
    public Weblog getPojo() {
        return this.pojo;
    }
}
