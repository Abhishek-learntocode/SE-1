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

import org.apache.roller.weblogger.config.WebloggerRuntimeConfig;


/**
 * Utility class providing shared constants and helper methods for URL
 * construction across different URLStrategy implementations.
 *
 * <p>This class was extracted from {@code AbstractURLStrategy} during
 * refactoring to eliminate a broken hierarchy (Instance 5.2). It replaces
 * the abstract base class with a stateless utility, allowing
 * {@link MultiWeblogURLStrategy} to implement {@link URLStrategy} directly
 * without inheriting from an intermediate abstract class.</p>
 */
public final class URLBuilderUtils {

    /**
     * Default initial capacity for StringBuilder instances used in URL
     * construction.
     */
    public static final int URL_BUFFER_SIZE = 64;

    private URLBuilderUtils() {
        // Utility class — prevent instantiation
    }

    /**
     * Returns the absolute context URL for this Weblogger installation.
     *
     * @return absolute context URL (e.g., "https://example.com/roller")
     */
    public static String getAbsoluteUrl() {
        return WebloggerRuntimeConfig.getAbsoluteContextURL();
    }

    /**
     * Returns the relative context URL for this Weblogger installation.
     *
     * @return relative context URL (e.g., "/roller")
     */
    public static String getRelativeUrl() {
        return WebloggerRuntimeConfig.getRelativeContextURL();
    }

    /**
     * Creates a new StringBuilder pre-populated with the context URL
     * (absolute or relative based on the parameter).
     *
     * @param absolute true for absolute URL, false for relative
     * @return StringBuilder initialized with the appropriate context URL
     */
    public static StringBuilder startUrl(boolean absolute) {
        return new StringBuilder(
                absolute ? getAbsoluteUrl() : getRelativeUrl());
    }

}
