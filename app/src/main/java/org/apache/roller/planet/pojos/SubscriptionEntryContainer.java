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

package org.apache.roller.planet.pojos;

import java.util.Date;


/**
 * Interface representing the container (subscription) of a SubscriptionEntry.
 *
 * <p>This abstraction breaks the compile-time cyclic dependency between
 * {@code Subscription} and {@code SubscriptionEntry} by allowing
 * {@code SubscriptionEntry} to depend on this interface rather than the
 * concrete {@code Subscription} class.  At runtime the JPA provider
 * still injects full {@code Subscription} instances (which implement
 * this interface), so all persistence and template behaviour is preserved.</p>
 */
public interface SubscriptionEntryContainer {

    /**
     * Returns the unique identifier of the subscription.
     */
    String getId();

    /**
     * Returns the timestamp of the last update for this subscription.
     */
    Date getLastUpdated();

    /**
     * Returns the title of the subscription.
     */
    String getTitle();

    /**
     * Returns the feed URL of the subscription.
     */
    String getFeedURL();

    /**
     * Returns the site URL of the subscription.
     */
    String getSiteURL();

    /**
     * Returns the author of the subscription.
     */
    String getAuthor();
}
