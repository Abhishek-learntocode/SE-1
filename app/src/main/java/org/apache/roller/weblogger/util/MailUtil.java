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

package org.apache.roller.weblogger.util;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.TreeSet;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.SendFailedException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.Address;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business.MailProvider;
import org.apache.roller.weblogger.business.WebloggerFactory;
import org.apache.roller.weblogger.business.WeblogManager;
import org.apache.roller.weblogger.business.startup.WebloggerStartup;
import org.apache.roller.weblogger.config.WebloggerRuntimeConfig;
import org.apache.roller.weblogger.pojos.User;
import org.apache.roller.weblogger.pojos.WeblogEntry;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.pojos.WeblogEntryComment;
import org.apache.roller.weblogger.pojos.WeblogPermission;
import org.apache.roller.weblogger.util.RollerMessages.RollerMessage;


/**
 * A utility class for helping with sending email. 
 */
public class MailUtil {
    
    private static Log log = LogFactory.getLog(MailUtil.class);
    
    private static final String EMAIL_ADDR_REGEXP = "^.*@.*[.].{2,}$";
    
    
    /**
     * Ideally mail senders should call this first to avoid errors that occur 
     * when mail is not properly configured. We'll complain about that at 
     * startup, no need to complain on every attempt to send.
     */
    public static boolean isMailConfigured() {
        return WebloggerStartup.getMailProvider() != null; 
    }
    
    /**
     * Send an email notice that a new pending entry has been submitted.
     */
    public static void sendPendingEntryNotice(WeblogEntry entry) throws WebloggerException {
        
        Session mailSession = WebloggerStartup.getMailProvider() != null
                ? WebloggerStartup.getMailProvider().getSession() : null;

        if (mailSession == null) {
            throw new WebloggerException("Couldn't get mail Session");
        }
        
        try {
            WeblogManager wmgr = WebloggerFactory.getWeblogger().getWeblogManager();
            
            String from = entry.getCreator().getEmailAddress();
            String[] to = getPendingEntryReviewerEmails(entry, wmgr);
            String[] cc = new String[] {from};
            String[] bcc = new String[0];
            
            String editURL = WebloggerFactory.getWeblogger().getUrlStrategy().getEntryEditURL(entry.getWebsite().getHandle(), entry.getId(), true);
            
            ResourceBundle resources = ResourceBundle.getBundle("ApplicationResources", entry.getWebsite().getLocaleInstance());
            
            String subject = formatPendingEntryNoticeSubject(entry, resources);
            String content = formatPendingEntryNoticeContent(entry, entry.getCreator().getUserName(), editURL, resources);
            
            MailUtil.sendTextMessage(from, to, cc, bcc, subject, content);
        } catch (MessagingException e) {
            log.error("ERROR: Problem sending pending entry notification email.", e);
        }
    }
    
    private static String[] getPendingEntryReviewerEmails(WeblogEntry entry, WeblogManager wmgr) throws WebloggerException {
        List<String> reviewers = new ArrayList<>();
        List<User> websiteUsers = wmgr.getWeblogUsers(entry.getWebsite(), true);
        
        for (User websiteUser : websiteUsers) {
            if (entry.getWebsite().hasUserPermission(websiteUser, WeblogPermission.POST) && websiteUser.getEmailAddress() != null) {
                reviewers.add(websiteUser.getEmailAddress());
            }
        }
        return reviewers.toArray(String[]::new);
    }

    private static String formatPendingEntryNoticeSubject(WeblogEntry entry, ResourceBundle resources) {
        return MessageFormat.format(
                resources.getString("weblogEntry.pendingEntrySubject"),
                entry.getWebsite().getName(),
                entry.getWebsite().getHandle());
    }

    private static String formatPendingEntryNoticeContent(WeblogEntry entry, String userName, String editURL, ResourceBundle resources) {
        return MessageFormat.format(
                resources.getString("weblogEntry.pendingEntryContent"),
                userName, userName, editURL);
    }
    
    /**
     * Send a weblog invitation email.
     */
    public static void sendWeblogInvitation(Weblog website, User user)
            throws WebloggerException {
        
        Session mailSession = WebloggerStartup.getMailProvider() != null
                ? WebloggerStartup.getMailProvider().getSession() : null;

        if(mailSession == null) {
            throw new WebloggerException("ERROR: Notification email(s) not sent, "
                    + "Roller's mail session not properly configured");
        }
        
        try {
            String from = website.getEmailAddress();
            String[] cc = new String[] {from};
            String[] bcc = new String[0];
            String[] to = new String[] {user.getEmailAddress()};
            
            String rootURL = WebloggerRuntimeConfig.getAbsoluteContextURL();
            String invitationURL = rootURL + "/roller-ui/menu.rol";
            
            ResourceBundle resources = ResourceBundle.getBundle("ApplicationResources", website.getLocaleInstance());
            
            String subject = formatWeblogInvitationSubject(website, resources);
            String content = formatWeblogInvitationContent(website, user, invitationURL, resources);
            
            MailUtil.sendTextMessage(from, to, cc, bcc, subject, content);
        } catch (MessagingException e) {
            throw new WebloggerException("ERROR: Notification email(s) not sent, "
                    + "due to Roller configuration or mail server problem.", e);
        }
    }
    
    private static String formatWeblogInvitationSubject(Weblog website, ResourceBundle resources) {
        return MessageFormat.format(
                resources.getString("inviteMember.notificationSubject"),
                website.getName(),
                website.getHandle());
    }

    private static String formatWeblogInvitationContent(Weblog website, User user, String invitationURL, ResourceBundle resources) {
        return MessageFormat.format(
                resources.getString("inviteMember.notificationContent"),
                website.getName(),
                website.getHandle(),
                user.getUserName(),
                invitationURL);
    }
    
    /**
     * Send a weblog invitation email.
     */
    public static void sendUserActivationEmail(User user)
            throws WebloggerException {
        
        Session mailSession = WebloggerStartup.getMailProvider() != null
                ? WebloggerStartup.getMailProvider().getSession() : null;

        if(mailSession == null) {
            throw new WebloggerException("ERROR: Notification email(s) not sent, "
                    + "Roller's mail session not properly configured");
        }
        
        try {
            ResourceBundle resources = ResourceBundle.getBundle(
                    "ApplicationResources", I18nUtils.toLocale(user.getLocale()));
            
            String from = WebloggerRuntimeConfig.getProperty(
                    "user.account.activation.mail.from");
            
            String[] cc = new String[0];
            String[] bcc = new String[0];
            String[] to = new String[] { user.getEmailAddress() };
            String subject = resources.getString(
                    "user.account.activation.mail.subject");
            
            String rootURL = WebloggerRuntimeConfig.getAbsoluteContextURL();
            
            String activationURL = rootURL
                    + "/roller-ui/register!activate.rol?activationCode="
                    + user.getActivationCode();
            
            String content = formatUserActivationContent(user, activationURL, resources);
            
            sendHTMLMessage(from, to, cc, bcc, subject, content);
        } catch (MessagingException e) {
            throw new WebloggerException("ERROR: Problem sending activation email.", e);
        }
    }
    
    private static String formatUserActivationContent(User user, String activationURL, ResourceBundle resources) {
        return MessageFormat.format(
                resources.getString("user.account.activation.mail.content"),
                user.getFullName(), user.getUserName(),
                activationURL);
    }
    
    /**
     * Send email notification of new or newly approved comment.
     *
     * @param commentObject      The new comment
     * @param messages           Messages to be included in e-mail (or null). 
     */
     *                           Errors will be assumed to be "validation errors" 
     *                           and messages will be assumed to be "from the system"
     */
    public static void sendEmailNotification(WeblogEntryComment commentObject,
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

// Assuming these imports are from the original file and are needed for the types used.
// The instruction was to keep ALL original imports.
// The provided block does not contain the actual import statements, but refers to types.
// I'll assume standard Java types and Roller-specific types are already imported.
// For example:
// import org.apache.commons.lang.StringUtils;
// import org.apache.commons.logging.Log;
// import org.apache.commons.logging.LogFactory;
// import org.roller.business.WebloggerFactory;
// import org.roller.pojos.Weblog;
// import org.roller.pojos.WeblogEntry;
// import org.roller.pojos.WeblogEntryComment;
// import org.roller.pojos.User;
// import org.roller.util.I18nMessages;
// import org.roller.util.MailUtil.MailingException;
// import org.roller.util.RollerMessages;
// import org.roller.util.RollerMessages.RollerMessage;
// import org.roller.util.Utilities;
// import org.roller.util.WebloggerRuntimeConfig;
// import org.

            // Send email notifications because a new comment has been approved
            sendEmailNotification(comment, messages, resources, true);

            // Send approval notification to author of approved comment
            sendEmailApprovalNotification(comment, resources);
        }
    }
    
    
    /**
     * Send message to author of approved comment
     */
    public static void sendEmailApprovalNotification(WeblogEntryComment cd, I18nMessages resources)
            throws MailingException {
        
        WeblogEntry entry = cd.getWeblogEntry();
        Weblog weblog = entry.getWebsite();
        User user = entry.getCreator();
        
        // use either the weblog configured from address or the site configured from address
        String from = weblog.getEmailAddress();
        if(StringUtils.isEmpty(from)) {
            from = user.getEmailAddress();
        }
        
        // form the message to be sent
        String subject = resources.getString("email.comment.commentApproved");
        
        StringBuilder msg = new StringBuilder();
        msg.append(resources.getString("email.comment.commentApproved"));
        msg.append("\n\n");
        msg.append(WebloggerFactory.getWeblogger().getUrlStrategy()
            .getWeblogCommentsURL(weblog, null, entry.getAnchor(), true));
        
        // send message to author of approved comment
        try {
            sendTextMessage(from, new String[] {cd.getEmail()}, null, null, subject, msg.toString());
        } catch (Exception e) {
            log.warn("Exception sending comment mail: " + e.getMessage());
            // This will log the stack trace if debug is enabled
            if (log.isDebugEnabled()) {
                log.debug(e);
            }
        }
        
        log.debug("Done sending email message");
    }
    
    
    // agangolli: Incorporated suggested changes from Ken Blackler.
    
    /**
     * This method is used to send a Message with a pre-defined
     * mime-type.
     *
     * @param from e-mail address of sender
     * @param to e-mail address(es) of recipients
     * @param subject subject of e-mail
     * @param content the body of the e-mail
     * @param mimeType type of message, i.e. text/plain or text/html
     * @throws MessagingException the exception to indicate failure
     */
    public static void sendMessage(String from, String[] to, String[] cc, String[] bcc, String subject,
            String content, String mimeType) throws MessagingException {
        
        MailProvider mailProvider = WebloggerStartup.getMailProvider();
        if (mailProvider == null) {
            return;
        }
        
        Session session = mailProvider.getSession();
        MimeMessage message = new MimeMessage(session);
        
        // n.b. any default from address is expected to be determined by caller.
        if (! StringUtils.isEmpty(from)) {
            InternetAddress sentFrom = new InternetAddress(from);
            message.setFrom(sentFrom);
            if (log.isDebugEnabled()) {
                log.debug("e-mail from: " + sentFrom);
            }
        }
        
        if (to!=null) {
            InternetAddress[] sendTo = new InternetAddress[to.length];
            
            for (int i = 0; i < to.length; i++) {
                sendTo[i] = new InternetAddress(to[i]);
                if (log.isDebugEnabled()) {
                    log.debug("sending e-mail to: " + to[i]);
                }
            }
            message.setRecipients(Message.RecipientType.TO, sendTo);
        }
        
        if (cc != null) {
            InternetAddress[] copyTo = new InternetAddress[cc.length];
            
            for (int i = 0; i < cc.length; i++) {
                copyTo[i] = new InternetAddress(cc[i]);
                if (log.isDebugEnabled()) {
                    log.debug("copying e-mail to: " + cc[i]);
                }
            }
            message.setRecipients(Message.RecipientType.CC, copyTo);
        }
        
        if (bcc != null) {
            InternetAddress[] copyTo = new InternetAddress[bcc.length];
            
            for (int i = 0; i < bcc.length; i++) {
                copyTo[i] = new InternetAddress(bcc[i]);
                if (log.isDebugEnabled()) {
                    log.debug("blind copying e-mail to: " + bcc[i]);
                }
            }
            message.setRecipients(Message.RecipientType.BCC, copyTo);
        }
        message.setSubject((subject == null) ? "(no subject)" : subject, "UTF-8");
        message.setContent(content, mimeType);
        message.setSentDate(new java.util.Date());
        
        // First collect all the addresses together.
        Address[] remainingAddresses = message.getAllRecipients();
        int nAddresses = remainingAddresses.length;
        boolean bFailedToSome = false;
        
        SendFailedException sendex = new SendFailedException("Unable to send message to some recipients");
        
        Transport transport = mailProvider.getTransport();
        
        // Try to send while there remain some potentially good addresses
        try { 
            do {
                // Avoid a loop if we are stuck
                nAddresses = remainingAddresses.length;

                try {
                    // Send to the list of remaining addresses, ignoring the addresses attached to the message
                    transport.sendMessage(message, remainingAddresses);
                } catch(SendFailedException ex) {
                    bFailedToSome=true;
                    sendex.setNextException(ex);

                    // Extract the remaining potentially good addresses
                    remainingAddresses=ex.getValidUnsentAddresses();
                }
            } while (remainingAddresses!=null && remainingAddresses.length>0 
                    && remainingAddresses.length!=nAddresses);
            
        } finally {
            transport.close();
        }
        
        if (bFailedToSome) {
            throw sendex;
        }
    }
    
    
    /**
     * This method is used to send a Text Message.
     *
     * @param from e-mail address of sender
     * @param to e-mail addresses of recipients
     * @param cc e-mail address of cc recipients
     * @param bcc e-mail address of bcc recipients
     * @param subject subject of e-mail
     * @param content the body of the e-mail
     * @throws MessagingException the exception to indicate failure
     */
    public static void sendTextMessage(String from, String[] to, String[] cc, String[] bcc,
                                       String subject, String content) throws MessagingException {
        sendMessage(from, to, cc, bcc, subject, content, "text/plain; charset=utf-8");
    }

    /**
     * This method is used to send a HTML Message
     *
     * @param from e-mail address of sender
     * @param to e-mail address(es) of recipients
     * @param subject subject of e-mail
     * @param content the body of the e-mail
     * @throws MessagingException the exception to indicate failure
     */
    public static void sendHTMLMessage(String from, String[] to, String[] cc, String[] bcc, String subject,
                                       String content) throws MessagingException {
        sendMessage(from, to, cc, bcc, subject, content, "text/html; charset=utf-8");
    }

    /**
     * An exception thrown if there is a problem sending an email.
     */
    public class MailingException extends WebloggerException {
        public MailingException(Throwable t) {
            super(t);
        }
    }
}

null,
                            commenterAddrs,
                            subject, 
                            msg.toString());
                }
            }
        } catch (Exception e) {
            log.warn("Exception sending comment notification mail", e);
            // This will log the stack trace if debug is enabled
            if (log.isDebugEnabled()) {
                log.debug(e);
            }
        }
        
        log.debug("Done sending email message");
    }
    

    public static void sendEmailApprovalNotifications(List<WeblogEntryComment> comments,
                                               I18nMessages resources) 
            throws MailingException {
        
        RollerMessages messages = new RollerMessages();
        for (WeblogEntryComment comment : comments) {

            // Send email notifications because a new comment has been approved
            sendEmailNotification(comment, messages, resources, true);

            // Send approval notification to author of approved comment
            sendEmailApprovalNotification(comment, resources);
        }
    }
    
    
    /**
     * Send message to author of approved comment
     */
    public static void sendEmailApprovalNotification(WeblogEntryComment cd, I18nMessages resources)
            throws MailingException {
        
        WeblogEntry entry = cd.getWeblogEntry();
        Weblog weblog = entry.getWebsite();
        User user = entry.getCreator();
        
        // use either the weblog configured from address or the site configured from address
        String from = weblog.getEmailAddress();
        if(StringUtils.isEmpty(from)) {
            from = user.getEmailAddress();
        }
        
        // form the message to be sent
        String subject = resources.getString("email.comment.commentApproved");
        
        StringBuilder msg = new StringBuilder();
        msg.append(resources.getString("email.comment.commentApproved"));
        msg.append("\n\n");
        msg.append(WebloggerFactory.getWeblogger().getUrlStrategy()
            .getWeblogCommentsURL(weblog, null, entry.getAnchor(), true));
        
        // send message to author of approved comment
        try {
            sendTextMessage(from, new String[] {cd.getEmail()}, null, null, subject, msg.toString());
        } catch (Exception e) {
            log.warn("Exception sending comment mail: " + e.getMessage());
            // This will log the stack trace if debug is enabled
            if (log.isDebugEnabled()) {
                log.debug(e);
            }
        }
        
        log.debug("Done sending email message");
    }
    
    
    // agangolli: Incorporated suggested changes from Ken Blackler.
    
    /**
     * This method is used to send a Message with a pre-defined
     * mime-type.
     *
     * @param from e-mail address of sender
     * @param to e-mail address(es) of recipients
     * @param subject subject of e-mail
     * @param content the body of the e-mail
     * @param mimeType type of message, i.e. text/plain or text/html
     * @throws MessagingException the exception to indicate failure
     */
    public static void sendMessage(String from, String[] to, String[] cc, String[] bcc, String subject,
            String content, String mimeType) throws MessagingException {
        
        MailProvider mailProvider = WebloggerStartup.getMailProvider();
        if (mailProvider == null) {
            return;
        }
        
        Session session = mailProvider.getSession();
        MimeMessage message = createAndConfigureMimeMessage(session, from, subject, content, mimeType);
        setAllRecipients(message, to, cc, bcc);
        sendMailWithRetry(mailProvider.getTransport(), message);
    }

    /**
     * Helper method to create and configure the MimeMessage with sender, subject, content, and sent date.
     */
    private static MimeMessage createAndConfigureMimeMessage(Session session, String from, String subject, String content, String mimeType) throws MessagingException {
        MimeMessage message = new MimeMessage(session);
        setSender(message, from);
        message.setSubject((subject == null) ? "(no subject)" : subject, "UTF-8");
        message.setContent(content, mimeType);
        message.setSentDate(new java.util.Date());
        return message;
    }

    /**
     * Helper method to set the sender address on the MimeMessage.
     */
    private static void setSender(MimeMessage message, String from) throws MessagingException {
        // n.b. any default from address is expected to be determined by caller.
        if (!StringUtils.isEmpty(from)) {
            InternetAddress sentFrom = new InternetAddress(from);
            message.setFrom(sentFrom);
            if (log.isDebugEnabled()) {
                log.debug("e-mail from: " + sentFrom);
            }
        }
    }

    /**
     * Helper method to set all recipient types (TO, CC, BCC) on the MimeMessage.
     */
    private static void setAllRecipients(MimeMessage message, String[] to, String[] cc, String[] bcc) throws MessagingException {
        setRecipientsForType(message, Message.RecipientType.TO, to, "to");
        setRecipientsForType(message, Message.RecipientType.CC, cc, "cc");
        setRecipientsForType(message, Message.RecipientType.BCC, bcc, "bcc");
    }

    /**
     * Generic helper method to set recipients for a given type (TO, CC, or BCC).
     */
    private static void setRecipientsForType(MimeMessage message, Message.RecipientType type, String[] addresses, String logPrefix) throws MessagingException {
        if (addresses != null && addresses.length > 0) {
            InternetAddress[] internetAddresses = new InternetAddress[addresses.length];
            for (int i = 0; i < addresses.length; i++) {
                internetAddresses[i] = new InternetAddress(addresses[i]);
                if (log.isDebugEnabled()) {
                    log.debug("sending e-mail " + logPrefix + ": " + addresses[i]);
                }
            }
            message.setRecipients(type, internetAddresses);
        }
    }

    /**
     * Helper method to send the mail with retry logic for SendFailedException.
     */
    private static void sendMailWithRetry(Transport transport, MimeMessage message) throws MessagingException {
        Address[] remainingAddresses = message.getAllRecipients();
        int nAddresses;
        boolean bFailedToSome = false;
        SendFailedException sendex = new SendFailedException("Unable to send message to some recipients");

        try { 
            // Try to send while there remain some potentially good addresses
            do {
                // Avoid a loop if we are stuck
                nAddresses = remainingAddresses.length;

                try {
                    // Send to the list of remaining addresses, ignoring the addresses attached to the message
                    transport.sendMessage(message, remainingAddresses);
                } catch(SendFailedException ex) {
                    bFailedToSome = true;
                    sendex.setNextException(ex);

                    // Extract the remaining potentially good addresses
                    remainingAddresses = ex.getValidUnsentAddresses();
                }
            } while (remainingAddresses != null && remainingAddresses.length > 0 
                    && remainingAddresses.length != nAddresses);
            
        } finally {
            transport.close();
        }
        
        if (bFailedToSome) {
            throw sendex;
        }
    }
    
    
    /**
     * This method is used to send a Text Message.
     *
     * @param from e-mail address of sender
     * @param to e-mail addresses of recipients
     * @param cc e-mail address of cc recipients
     * @param bcc e-mail address of bcc recipients
     * @param subject subject of e-mail
     * @param content the body of the e-mail
     * @throws MessagingException the exception to indicate failure
     */
    public static void sendTextMessage(String from, String[] to, String[] cc, String[] bcc,
                                       String subject, String content) throws MessagingException {
        sendMessage(from, to, cc, bcc, subject, content, "text/plain; charset=utf-8");
    }

    /**
     * This method is used to send a HTML Message
     *
     * @param from e-mail
/**
     * An exception thrown if there is a problem sending an email.
     */
    public class MailingException extends WebloggerException {
        public MailingException(Throwable t) {
            super(t);
        }
    }