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

import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.TreeSet;

import org.apache.commons.lang3.StringUtils;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.util.Utilities;

/**
 * Helper class that encapsulates tag lifecycle management logic
 * previously embedded in the {@link WeblogEntry} POJO.
 *
 * <p>This class was extracted as part of an Insufficient Modularization refactoring
 * (Instance 1.2) to separate tag management concerns from the data entity.
 * All methods are static and take a {@link WeblogEntry} parameter, preserving
 * the original logic verbatim.</p>
 *
 * <p>The tag fields ({@code tagSet}, {@code addedTags}, {@code removedTags}) remain
 * on {@link WeblogEntry} because they are part of the JPA entity mapping. This
 * handler operates on them through the entry's public accessors.</p>
 */
public final class WeblogEntryTagHandler {

    private WeblogEntryTagHandler() {
        // Utility class — prevent instantiation
    }

    /**
     * Roller lowercases all tags based on locale because there's not a 1:1 mapping
     * between uppercase/lowercase characters across all languages.
     * @param entry the weblog entry to add the tag to
     * @param name the tag name
     * @throws WebloggerException
     */
    public static void addTag(WeblogEntry entry, String name) throws WebloggerException {
        Locale localeObject = entry.getWebsite() != null ? entry.getWebsite().getLocaleInstance() : Locale.getDefault();
        name = Utilities.normalizeTag(name, localeObject);
        if (name.length() == 0) {
            return;
        }

        for (WeblogEntryTag tag : entry.getTags()) {
            if (tag.getName().equals(name)) {
                return;
            }
        }

        WeblogEntryTag tag = new WeblogEntryTag();
        tag.setName(name);
        tag.setCreatorUserName(entry.getCreatorUserName());
        tag.setWeblog(entry.getWebsite());
        tag.setWeblogEntry(entry);
        tag.setTime(entry.getUpdateTime());
        entry.getTags().add(tag);

        entry.getAddedTags().add(tag);
    }

    /**
     * Returns the tags as a space-separated string, sorted by name.
     * @param entry the weblog entry
     * @return tags as string
     */
    public static String getTagsAsString(WeblogEntry entry) {
        StringBuilder sb = new StringBuilder();
        // Sort by name
        Set<WeblogEntryTag> tmp = new TreeSet<>(new WeblogEntryTagComparator());
        tmp.addAll(entry.getTags());
        for (WeblogEntryTag entryTag : tmp) {
            sb.append(entryTag.getName()).append(" ");
        }
        if (sb.length() > 0) {
            sb.deleteCharAt(sb.length() - 1);
        }

        return sb.toString();
    }

    /**
     * Sets the tags from a string representation, managing the added/removed tracking sets.
     * @param entry the weblog entry
     * @param tags comma or space separated tag string
     * @throws WebloggerException
     */
    public static void setTagsAsString(WeblogEntry entry, String tags) throws WebloggerException {
        if (StringUtils.isEmpty(tags)) {
            entry.getRemovedTags().addAll(entry.getTags());
            entry.getTags().clear();
            return;
        }

        List<String> updatedTags = Utilities.splitStringAsTags(tags);
        Set<String> newTags = new HashSet<>(updatedTags.size());
        Locale localeObject = entry.getWebsite() != null ? entry.getWebsite().getLocaleInstance() : Locale.getDefault();

        for (String name : updatedTags) {
            newTags.add(Utilities.normalizeTag(name, localeObject));
        }

        // remove old ones no longer passed.
        for (Iterator<WeblogEntryTag> it = entry.getTags().iterator(); it.hasNext();) {
            WeblogEntryTag tag = it.next();
            if (!newTags.contains(tag.getName())) {
                // tag no longer listed in UI, needs removal from DB
                entry.getRemovedTags().add(tag);
                it.remove();
            } else {
                // already in persisted set, therefore isn't new
                newTags.remove(tag.getName());
            }
        }

        for (String newTag : newTags) {
            addTag(entry, newTag);
        }
    }

}
