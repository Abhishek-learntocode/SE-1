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

package org.apache.roller.weblogger.business;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business.jpa.JPAPersistenceStrategy;
import org.apache.roller.weblogger.business.pings.AutoPingManager;
import org.apache.roller.weblogger.business.pings.PingTargetManager;
import org.apache.roller.weblogger.config.WebloggerConfig;
import org.apache.roller.weblogger.pojos.AutoPing;
import org.apache.roller.weblogger.pojos.PingTarget;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.pojos.WeblogBookmark;
import org.apache.roller.weblogger.pojos.WeblogBookmarkFolder;
import org.apache.roller.weblogger.pojos.WeblogCategory;
import org.apache.roller.weblogger.pojos.WeblogPermission;


/**
 * Service for initializing default weblog contents during weblog creation.
 *
 * Extracted from JPAWeblogManagerImpl to resolve Feature Envy smell:
 * the addWeblogContents() method was more interested in members of the
 * Weblogger facade (accessing 4+ managers through it) than in its own
 * class's state. This class receives the required managers via constructor
 * injection, eliminating the Law of Demeter violations and Feature Envy.
 *
 * Responsibilities:
 * - Grant ADMIN permission to weblog creator
 * - Create default categories from configuration
 * - Create default bookmark folder and bookmarks from configuration
 * - Create default media file directory
 * - Configure auto-enabled ping targets
 */
@com.google.inject.Singleton
public class WeblogSetupService {

    private static final Log LOG = LogFactory.getLog(WeblogSetupService.class);

    private final JPAPersistenceStrategy strategy;
    private final UserManager userManager;
    private final MediaFileManager mediaFileManager;
    private final PingTargetManager pingTargetManager;
    private final AutoPingManager autoPingManager;

    @com.google.inject.Inject
    public WeblogSetupService(JPAPersistenceStrategy strategy,
                              UserManager userManager,
                              MediaFileManager mediaFileManager,
                              PingTargetManager pingTargetManager,
                              AutoPingManager autoPingManager) {
        LOG.debug("Instantiating WeblogSetupService");
        this.strategy = strategy;
        this.userManager = userManager;
        this.mediaFileManager = mediaFileManager;
        this.pingTargetManager = pingTargetManager;
        this.autoPingManager = autoPingManager;
    }

    /**
     * Initialize default contents for a newly created weblog.
     *
     * This method assumes the weblog entity has already been stored and
     * flushed in the persistence context before being called.
     *
     * @param newWeblog the weblog to initialize with default contents
     * @throws WebloggerException if any initialization step fails
     */
    public void initializeWeblogContents(Weblog newWeblog) throws WebloggerException {

        // grant weblog creator ADMIN permission
        grantOwnerPermission(newWeblog);

        // create default categories from configuration
        WeblogCategory firstCat = createDefaultCategories(newWeblog);

        // Use first category as default for Blogger API
        if (firstCat != null) {
            newWeblog.setBloggerCategory(firstCat);
        }

        this.strategy.store(newWeblog);

        // add default bookmarks
        createDefaultBookmarks(newWeblog);

        // create default media file directory
        mediaFileManager.createDefaultMediaFileDirectory(newWeblog);

        // flush so that all data up to this point can be available in db
        this.strategy.flush();

        // add any auto enabled ping targets
        configureAutoPingTargets(newWeblog);
    }

    /**
     * Grant ADMIN permission to the weblog's creator.
     */
    private void grantOwnerPermission(Weblog newWeblog) throws WebloggerException {
        List<String> actions = new ArrayList<>();
        actions.add(WeblogPermission.ADMIN);
        userManager.grantWeblogPermission(
                newWeblog, userManager.getUserByUserName(newWeblog.getCreatorUserName()), actions);
    }

    /**
     * Create default categories based on the "newuser.categories" configuration property.
     *
     * @return the first category created (used as default Blogger API category), or null
     */
    private WeblogCategory createDefaultCategories(Weblog newWeblog) throws WebloggerException {
        String cats = WebloggerConfig.getProperty("newuser.categories");
        WeblogCategory firstCat = null;
        if (cats != null) {
            String[] splitcats = cats.split(",");
            for (String split : splitcats) {
                if (split.isBlank()) {
                    continue;
                }
                WeblogCategory c = new WeblogCategory(
                        newWeblog,
                        split,
                        null,
                        null );
                if (firstCat == null) {
                    firstCat = c;
                }
                this.strategy.store(c);
            }
        }
        return firstCat;
    }

    /**
     * Create default bookmark folder and bookmarks based on the "newuser.blogroll"
     * configuration property.
     */
    private void createDefaultBookmarks(Weblog newWeblog) throws WebloggerException {
        WeblogBookmarkFolder defaultFolder = new WeblogBookmarkFolder(
                "default", newWeblog);
        this.strategy.store(defaultFolder);

        String blogroll = WebloggerConfig.getProperty("newuser.blogroll");
        if (blogroll != null) {
            String[] splitroll = blogroll.split(",");
            for (String splitItem : splitroll) {
                String[] rollitems = splitItem.split("\\|");
                if (rollitems.length > 1) {
                    WeblogBookmark b = new WeblogBookmark(
                            defaultFolder,
                            rollitems[0],
                            "",
                            rollitems[1].trim(),
                            null,
                            null);
                    this.strategy.store(b);
                }
            }
        }
    }

    /**
     * Configure auto-enabled ping targets for the new weblog.
     */
    private void configureAutoPingTargets(Weblog newWeblog) throws WebloggerException {
        for (PingTarget pingTarget : pingTargetManager.getCommonPingTargets()) {
            if(pingTarget.isAutoEnabled()) {
                AutoPing autoPing = new AutoPing(
                        null, pingTarget, newWeblog);
                autoPingManager.saveAutoPing(autoPing);
            }
        }
    }
}
