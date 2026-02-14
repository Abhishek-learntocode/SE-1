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

package org.apache.roller.weblogger.ui.rendering.util;

import java.util.Locale;
import org.apache.roller.weblogger.pojos.User;
import org.apache.roller.weblogger.pojos.Weblog;


/**
 * Common contract for weblog request objects.
 *
 * This interface captures the shared behavioral contract between
 * WeblogRequest (and its subclasses like WeblogFeedRequest) and
 * WeblogPageRequest (which uses composition rather than inheritance
 * to access WeblogRequest functionality).
 *
 * Introduced to break the broken hierarchy where WeblogPageRequest
 * extended WeblogRequest without overriding any of its methods.
 */
public interface WeblogRequestContext {

    /**
     * Get the weblog handle parsed from the request URL.
     */
    String getWeblogHandle();

    /**
     * Get the locale string parsed from the request URL, if any.
     */
    String getLocale();

    /**
     * Get the Weblog object for this request (lazily loaded from handle).
     */
    Weblog getWeblog();

    /**
     * Get the Locale instance for this request.
     */
    Locale getLocaleInstance();

    /**
     * Get the authenticated user name, if any.
     */
    String getAuthenticUser();

    /**
     * Get the authenticated User object, if any (lazily loaded).
     */
    User getUser();

    /**
     * Check if the request has an authenticated user.
     */
    boolean isLoggedIn();

}
