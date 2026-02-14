/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  The ASF licenses this file to You
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

package org.apache.roller.weblogger.pojos;

import java.util.List;
import java.util.Map;

import org.apache.commons.text.StringEscapeUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.roller.util.RollerConstants;
import org.apache.roller.weblogger.business.WebloggerFactory;
import org.apache.roller.weblogger.business.plugins.PluginManager;
import org.apache.roller.weblogger.business.plugins.entry.WeblogEntryPlugin;
import org.apache.roller.weblogger.util.HTMLSanitizer;
import org.apache.roller.weblogger.util.I18nMessages;
import org.apache.roller.weblogger.util.Utilities;

/**
 * Helper class that encapsulates content transformation and presentation logic
 * previously embedded in the {@link WeblogEntry} POJO.
 *
 * <p>This class was extracted as part of an Insufficient Modularization refactoring
 * (Instance 1.2) to separate presentation concerns from the data entity.
 * All methods are static and take a {@link WeblogEntry} parameter, preserving
 * the original logic verbatim.</p>
 */
public final class WeblogEntryContentHelper {

    private static final Log mLogger = LogFactory.getFactory().getInstance(WeblogEntryContentHelper.class);

    private WeblogEntryContentHelper() {
        // Utility class — prevent instantiation
    }

    /**
     * Get entry text, transformed by plugins enabled for entry.
     */
    public static String transformText(WeblogEntry entry) {
        return render(entry, entry.getText());
    }

    /**
     * Get entry summary, transformed by plugins enabled for entry.
     */
    public static String transformSummary(WeblogEntry entry) {
        return render(entry, entry.getSummary());
    }

    /**
     * Return the Title of this post, or the first 255 characters of the
     * entry's text.
     *
     * @return String
     */
    public static String getDisplayTitle(WeblogEntry entry) {
        if (entry.getTitle() == null || entry.getTitle().isBlank()) {
            return StringUtils.left(Utilities.removeHTML(entry.getText()), RollerConstants.TEXTWIDTH_255);
        }
        return Utilities.removeHTML(entry.getTitle());
    }

    /**
     * Return RSS 09x style description (escaped HTML version of entry text)
     */
    public static String getRss09xDescription(WeblogEntry entry) {
        return getRss09xDescription(entry, -1);
    }

    /**
     * Return RSS 09x style description (escaped HTML version of entry text)
     */
    public static String getRss09xDescription(WeblogEntry entry, int maxLength) {
        String ret = StringEscapeUtils.escapeHtml3(entry.getText());
        if (maxLength != -1 && ret.length() > maxLength) {
            ret = ret.substring(0, maxLength - 3) + "...";
        }
        return ret;
    }

    /**
     * Get the right transformed display content depending on the situation.
     *
     * If the readMoreLink is specified then we assume the caller wants to
     * prefer summary over content and we include a "Read More" link at the
     * end of the summary if it exists.  Otherwise, if the readMoreLink is
     * empty or null then we assume the caller prefers content over summary.
     */
    public static String displayContent(WeblogEntry entry, String readMoreLink) {

        String content;

        if (readMoreLink == null || readMoreLink.isBlank() || "nil".equals(readMoreLink)) {

            // no readMore link means permalink, so prefer text over summary
            if (StringUtils.isNotEmpty(entry.getText())) {
                content = transformText(entry);
            } else {
                content = transformSummary(entry);
            }
        } else {
            // not a permalink, so prefer summary over text
            // include a "read more" link if needed
            if (StringUtils.isNotEmpty(entry.getSummary())) {
                content = transformSummary(entry);
                if (StringUtils.isNotEmpty(entry.getText())) {
                    // add read more
                    List<String> args = List.of(readMoreLink);

                    // TODO: we need a more appropriate way to get the view locale here
                    String readMore = I18nMessages.getMessages(entry.getWebsite().getLocaleInstance()).getString("macro.weblog.readMoreLink", args);

                    content += readMore;
                }
            } else {
                content = transformText(entry);
            }
        }

        return HTMLSanitizer.conditionallySanitize(content);
    }

    /**
     * Get the right transformed display content.
     */
    public static String getDisplayContent(WeblogEntry entry) {
        return displayContent(entry, null);
    }

    /**
     * Transform string based on plugins enabled for this weblog entry.
     */
    private static String render(WeblogEntry entry, String str) {
        String ret = str;
        mLogger.debug("Applying page plugins to string");
        Map<String, WeblogEntryPlugin> inPlugins = null;
        try {
            PluginManager ppmgr = WebloggerFactory.getWeblogger().getPluginManager();
            inPlugins = ppmgr.getWeblogEntryPlugins(entry.getWebsite());
        } catch (Exception e) {
            mLogger.error("ERROR: initializing plugins");
        }
        if (str != null && inPlugins != null) {
            List<String> entryPlugins = entry.getPluginsList();

            // if no Entry plugins, don't bother looping.
            if (entryPlugins != null && !entryPlugins.isEmpty()) {

                // now loop over mPagePlugins, matching
                // against Entry plugins (by name):
                // where a match is found render Plugin.
                for (Map.Entry<String, WeblogEntryPlugin> mapEntry : inPlugins.entrySet()) {
                    if (entryPlugins.contains(mapEntry.getKey())) {
                        WeblogEntryPlugin pagePlugin = mapEntry.getValue();
                        try {
                            ret = pagePlugin.render(entry, ret);
                        } catch (Exception e) {
                            mLogger.error("ERROR from plugin: " + pagePlugin.getName(), e);
                        }
                    }
                }
            }
        }
        return HTMLSanitizer.conditionallySanitize(ret);
    }

}
