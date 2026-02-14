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

package org.apache.roller.weblogger.business;

import java.util.Date;
import java.util.List;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.pojos.CommentSearchCriteria;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.pojos.WeblogEntry;
import org.apache.roller.weblogger.pojos.WeblogEntryComment;
import org.apache.roller.weblogger.pojos.WeblogEntryComment.ApprovalStatus;


/**
 * Interface to comment management operations.
 * Extracted from WeblogEntryManager to separate comment concerns.
 */
public interface CommentManager {

    /**
     * Save comment.
     */
    void saveComment(WeblogEntryComment comment) throws WebloggerException;

    /**
     * Remove comment.
     */
    void removeComment(WeblogEntryComment comment) throws WebloggerException;

    /**
     * Get comment by id.
     */
    WeblogEntryComment getComment(String id) throws WebloggerException;

    /**
     * Generic comments query method.
     * @param csc CommentSearchCriteria object with fields indicating search criteria
     * @return list of comments fitting search criteria
     */
    List<WeblogEntryComment> getComments(CommentSearchCriteria csc) throws WebloggerException;

    /**
     * Deletes comments that match parameters.
     * @param website    Website or null for all comments on site
     * @param entry      Entry or null to include all comments
     * @param searchString Search string or null
     * @param startDate  Start date or null for no restriction
     * @param endDate    End date or null for no restriction
     * @param status     Status of comment
     * @return Number of comments deleted
     */
    int removeMatchingComments(
            Weblog website,
            WeblogEntry entry,
            String searchString,
            Date startDate,
            Date endDate,
            ApprovalStatus status
    ) throws WebloggerException;

    /**
     * Get site-wide comment count.
     */
    long getCommentCount() throws WebloggerException;

    /**
     * Get weblog comment count.
     */
    long getCommentCount(Weblog website) throws WebloggerException;
}
