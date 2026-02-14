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

import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.roller.weblogger.WebloggerException;
import org.apache.roller.weblogger.business.FileContentManager;
import org.apache.roller.weblogger.business.MediaFileManager;
import org.apache.roller.weblogger.business.WeblogManager;
import org.apache.roller.weblogger.business.Weblogger;
import org.apache.roller.weblogger.business.WebloggerFactory;
import org.apache.roller.weblogger.config.WebloggerConfig;
import org.apache.roller.weblogger.pojos.MediaFile;
import org.apache.roller.weblogger.pojos.MediaFileDirectory;
import org.apache.roller.weblogger.pojos.Weblog;
import org.apache.roller.weblogger.util.RollerMessages;

import com.google.inject.Inject;
import com.google.inject.Singleton;

@Singleton
public class JPAMediaFileManagerImpl implements MediaFileManager {

    private final Weblogger roller;
    private final JPAPersistenceStrategy strategy;
    private static final Log log = LogFactory.getFactory().getInstance(JPAMediaFileManagerImpl.class);
    public static final String MIGRATION_STATUS_FILENAME = "migration-status.properties";

    /**
     * Creates a new instance of MediaFileManagerImpl
     */
    @Inject
    protected JPAMediaFileManagerImpl(Weblogger roller,
            JPAPersistenceStrategy persistenceStrategy) {
        this.roller = roller;
        this.strategy = persistenceStrategy;
    }

    /**
     * Initialize manager; deal with upgrade/migration if 'uploads.migrate.auto'
     * is true.
     */
    @Override
    public void initialize() {
        boolean autoUpgrade = WebloggerConfig
                .getBooleanProperty("uploads.migrate.auto");
        if (autoUpgrade && this.isFileStorageUpgradeRequired()) {
            this.upgradeFileStorage();
        }
    }

    /**
     * Release resources; currently a no-op.
     */
    @Override
    public void release() {
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void moveMediaFiles(Collection<MediaFile> mediaFiles,
            MediaFileDirectory targetDirectory) throws WebloggerException {

        List<MediaFile> moved = new ArrayList<>(mediaFiles);

        for (MediaFile mediaFile : moved) {
            mediaFile.getDirectory().getMediaFiles().remove(mediaFile);

            mediaFile.setDirectory(targetDirectory);
            this.strategy.store(mediaFile);

            targetDirectory.getMediaFiles().add(mediaFile);
            this.strategy.store(targetDirectory);
        }
        // update weblog last modified date. date updated by saveWebsite()
        roller.getWeblogManager().saveWeblog(targetDirectory.getWeblog());

        // Refresh associated parent for changes
        roller.flush();
        if (!moved.isEmpty()) {
            strategy.refresh(moved.get(0).getDirectory());
        }

        // Refresh associated parent for changes
        strategy.refresh(targetDirectory);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void moveMediaFile(MediaFile mediaFile,
            MediaFileDirectory targetDirectory) throws WebloggerException {
        moveMediaFiles(Arrays.asList(mediaFile), targetDirectory);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void createMediaFileDirectory(MediaFileDirectory directory)
            throws WebloggerException {
        this.strategy.store(directory);

        // update weblog last modified date. date updated by saveWebsite()
        roller.getWeblogManager().saveWeblog(directory.getWeblog());

        // Refresh associated parent for changes
        // strategy.refresh(directory.getParent());
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFileDirectory createMediaFileDirectory(Weblog weblog,
            String requestedName) throws WebloggerException {

        requestedName = requestedName.startsWith("/") ? requestedName.substring(1) : requestedName;

        if (requestedName.isEmpty() || requestedName.equals("default")) {
            // Default cannot be created using this method.
            // Use createDefaultMediaFileDirectory instead
            throw new WebloggerException("Invalid name!");
        }

        MediaFileDirectory newDirectory;

        if (weblog.hasMediaFileDirectory(requestedName)) {
            throw new WebloggerException("Directory exists");
        } else {
            newDirectory = new MediaFileDirectory(weblog, requestedName, null);
            log.debug("Created new Directory " + requestedName);
        }

        // update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);

        return newDirectory;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFileDirectory createDefaultMediaFileDirectory(Weblog weblog)
            throws WebloggerException {
        MediaFileDirectory defaultDirectory = new MediaFileDirectory(weblog, "default",
                "default directory");
        createMediaFileDirectory(defaultDirectory);
        return defaultDirectory;
    }

    /**
     * Helper method to save a media file and perform common post-save operations.
     */
    private void saveMediaFileInternal(Weblog weblog, MediaFile mediaFile, FileContentManager cmgr) throws WebloggerException {
        strategy.store(mediaFile);

        // Refresh associated parent for changes
        roller.flush();
        strategy.refresh(mediaFile.getDirectory());

        // update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);

        cmgr.saveFileContent(weblog, mediaFile.getId(), mediaFile.getInputStream());

        if (mediaFile.isImageFile()) {
            updateThumbnail(mediaFile);
        }
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void createMediaFile(Weblog weblog, MediaFile mediaFile,
            RollerMessages errors) throws WebloggerException {

        FileContentManager cmgr = WebloggerFactory.getWeblogger()
                .getFileContentManager();
        if (!cmgr.canSave(weblog, mediaFile.getName(),
                mediaFile.getContentType(), mediaFile.getLength(), errors)) {
            return;
        }
        saveMediaFileInternal(weblog, mediaFile, cmgr);
    }

    @Override
    public void createThemeMediaFile(Weblog weblog, MediaFile mediaFile,
                                RollerMessages errors) throws WebloggerException {

        FileContentManager cmgr = WebloggerFactory.getWeblogger().getFileContentManager();
        saveMediaFileInternal(weblog, mediaFile, cmgr);
    }
}

    private void updateThumbnail(MediaFile mediaFile) {
        try {
            FileContentManager cmgr = WebloggerFactory.getWeblogger()
                    .getFileContentManager();
            FileContent fc = cmgr.getFileContent(mediaFile.getWeblog(),
                    mediaFile.getId());
            BufferedImage img;

            img = ImageIO.read(fc.getInputStream());

            // determine and save width and height
            mediaFile.setWidth(img.getWidth());
            mediaFile.setHeight(img.getHeight());
            strategy.store(mediaFile);

            int newWidth = mediaFile.getThumbnailWidth();
            int newHeight = mediaFile.getThumbnailHeight();

// update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);

        cmgr.saveFileContent(weblog, mediaFile.getId(),
            mediaFile.getInputStream());

        if (mediaFile.isImageFile()) {
            updateThumbnail(mediaFile);
        }
    }

    private void updateThumbnail(MediaFile mediaFile) {
        try {
            FileContentManager cmgr = WebloggerFactory.getWeblogger().getFileContentManager();

            BufferedImage originalImage = getAndValidateImage(mediaFile, cmgr);
            updateMediaFileDimensions(mediaFile, originalImage);
            createAndSaveThumbnailImage(mediaFile, originalImage, cmgr);
            performPostThumbnailSaveActions(mediaFile);

        } catch (Exception e) {
            log.debug("ERROR creating thumbnail", e);
        }
    }

    private BufferedImage getAndValidateImage(MediaFile mediaFile, FileContentManager cmgr) throws IOException, WebloggerException {
        FileContent fc = cmgr.getFileContent(mediaFile.getWeblog(), mediaFile.getId());
        BufferedImage img = ImageIO.read(fc.getInputStream());
        if (img == null) {
            throw new IOException("Could not read image from input stream for media file: " + mediaFile.getId());
        }
        return img;
    }

    private void updateMediaFileDimensions(MediaFile mediaFile, BufferedImage originalImage) throws WebloggerException {
        mediaFile.setWidth(originalImage.getWidth());
        mediaFile.setHeight(originalImage.getHeight());
        strategy.store(mediaFile);
    }

    private void createAndSaveThumbnailImage(MediaFile mediaFile, BufferedImage originalImage, FileContentManager cmgr) throws IOException, WebloggerException {
        int newWidth = mediaFile.getThumbnailWidth();
        int newHeight = mediaFile.getThumbnailHeight();

        Image newImage = originalImage.getScaledInstance(newWidth, newHeight, Image.SCALE_SMOOTH);
        BufferedImage tmp = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = tmp.createGraphics();
        try {
            g2.drawImage(newImage, 0, 0, newWidth, newHeight, null);
        } finally {
            g2.dispose();
        }

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(tmp, "png", baos);

        cmgr.saveFileContent(mediaFile.getWeblog(), mediaFile.getId() + "_sm", new ByteArrayInputStream(baos.toByteArray()));
    }

    private void performPostThumbnailSaveActions(MediaFile mediaFile) throws WebloggerException {
        roller.flush();
        strategy.refresh(mediaFile.getDirectory());
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void updateMediaFile(Weblog weblog, MediaFile mediaFile)
            throws WebloggerException {
        mediaFile.setLastUpdated(new Timestamp(System.currentTimeMillis()));
        strategy.store(mediaFile);

        roller.flush();
        // Refresh associated parent for changes
        strategy.refresh(mediaFile.getDirectory());

        // update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void updateMediaFile(Weblog weblog, MediaFile mediaFile,
            InputStream is) throws WebloggerException {
        mediaFile.setLastUpdated(new Timestamp(System.currentTimeMillis()));
        strategy.store(mediaFile);

        roller.flush();
        // Refresh associated parent for changes
        strategy.refresh(mediaFile.getDirectory());

        // update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);

        FileContentManager cmgr = WebloggerFactory.getWeblogger()
                .getFileContentManager();
        RollerMessages msgs = new RollerMessages();
        if (!cmgr.canSave(weblog, mediaFile.getName(),
                mediaFile.getContentType(), mediaFile.getLength(), msgs)) {
            throw new FileIOException(msgs.toString());
        }
        cmgr.saveFileContent(weblog, mediaFile.getId(), is);

        if (mediaFile.isImageFile()) {
            updateThumbnail(mediaFile);
        }
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFile getMediaFile(String id) throws WebloggerException {
        return getMediaFile(id, false);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFile getMediaFile(String id, boolean includeContent)
            throws WebloggerException {
        MediaFile mediaFile = (MediaFile) this.strategy.load(MediaFile.class,
                id);
        if (includeContent) {
            FileContentManager cmgr = WebloggerFactory.getWeblogger()
                    .getFileContentManager();

            FileContent content = cmgr.getFileContent(mediaFile.getDirectory()
                    .getWeblog(), id);
            mediaFile.setContent(content);

            try {
                FileContent thumbnail = cmgr.getFileContent(mediaFile
                        .getDirectory().getWeblog(), id + "_sm");
                mediaFile.setThumbnailContent(thumbnail);

            } catch (Exception e) {
                if (log.isDebugEnabled()) {
                    log.debug("Cannot load thumbnail for image " + id, e);
                } else {
                    log.warn("Cannot load thumbnail for image " + id);
                }
            }
        }
        return mediaFile;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFileDirectory getMediaFileDirectoryByName(Weblog weblog,
            String name) throws WebloggerException {

        name = name.startsWith("/") ? name.substring(1) : name;

        log.debug("Looking up weblog|media file directory: " + weblog.getHandle() + "|" + name);

        TypedQuery<MediaFileDirectory> q = this.strategy
                .getNamedQuery("MediaFileDirectory.getByWeblogAndName", MediaFileDirectory.class);
        q.setParameter(1, weblog);
        q.setParameter(2, name);
        try {
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFile getMediaFileByPath(Weblog weblog, String path)
            throws WebloggerException {

        // get directory
        String fileName = path;
        MediaFileDirectory mdir;
        int slash = path.lastIndexOf('/');
        if (slash > 0) {
            mdir = getMediaFileDirectoryByName(weblog, path.substring(0, slash));
        } else {
            mdir = getDefaultMediaFileDirectory(weblog);
        }
        if (slash != -1) {
            fileName = fileName.substring(slash + 1);
        }
        return mdir.getMediaFile(fileName);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFile getMediaFileByOriginalPath(Weblog weblog, String origpath)
            throws WebloggerException {

        if (null == origpath) {
            return null;
        }

        if (!origpath.startsWith("/")) {
            origpath = "/" + origpath;
        }

        TypedQuery<MediaFile> q = this.strategy
                .getNamedQuery("MediaFile.getByWeblogAndOrigpath", MediaFile.class);
        q.setParameter(1, weblog);
        q.setParameter(2, origpath);
        MediaFile mf;
        try {
            mf = q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
        FileContentManager cmgr = WebloggerFactory.getWeblogger()
                .getFileContentManager();
        FileContent content = cmgr.getFileContent(
                mf.getDirectory().getWeblog(), mf.getId());
        mf.setContent(content);
        return mf;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public MediaFileDirectory getMediaFileDirectory(String id)
            throws WebloggerException {
        return (MediaFileDirectory) this.strategy.load(
                MediaFileDirectory.class, id);
    }

    /**
     * {@inheritDoc}
public List<MediaFileDirectory> getMediaFileDirectories(Weblog weblog)
            throws WebloggerException {

        TypedQuery<MediaFileDirectory> q = this.strategy.getNamedQuery("MediaFileDirectory.getByWeblog",
                MediaFileDirectory.class);
        q.setParameter(1, weblog);
        return q.getResultList();
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void removeMediaFile(Weblog weblog, MediaFile mediaFile)
            throws WebloggerException {
        FileContentManager cmgr = WebloggerFactory.getWeblogger()
                .getFileContentManager();

        this.strategy.remove(mediaFile);

        // Refresh associated parent for changes
        strategy.refresh(mediaFile.getDirectory());

        // update weblog last modified date. date updated by saveWeblog()
        roller.getWeblogManager().saveWeblog(weblog);

        try {
            cmgr.deleteFile(weblog, mediaFile.getId());
            // Now thumbnail
            cmgr.deleteFile(weblog, mediaFile.getId() + "_sm");
        } catch (Exception e) {
            log.debug("File to be deleted already unavailable in the file store");
        }
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<MediaFile> fetchRecentPublicMediaFiles(int length)
            throws WebloggerException {

        String queryString = "SELECT m FROM MediaFile m WHERE m.sharedForGallery = true order by m.dateUploaded";
        TypedQuery<MediaFile> query = strategy.getDynamicQuery(queryString, MediaFile.class);
        query.setFirstResult(0);
        query.setMaxResults(length);
        return query.getResultList();
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<MediaFile> searchMediaFiles(Weblog weblog,
            MediaFileFilter filter) throws WebloggerException {

        List<Object> params = new ArrayList<>();
        AtomicInteger paramIndex = new AtomicInteger(0);
        StringBuilder whereClause = new StringBuilder("m.directory.weblog = ?");
        
        params.add(paramIndex.get(), weblog);
        whereClause.append(paramIndex.incrementAndGet());

        appendNameFilterClause(whereClause, params, paramIndex, filter.getName());
        appendSizeFilterClause(whereClause, params, paramIndex, filter);
        appendTagsFilterClause(whereClause, params, paramIndex, filter);
        appendTypeFilterClause(whereClause, params, paramIndex, filter);

        String orderByClause = buildOrderByClause(filter);

        String queryString = "SELECT m FROM MediaFile m WHERE " + whereClause.toString() + orderByClause;
        TypedQuery<MediaFile> query = strategy.getDynamicQuery(queryString, MediaFile.class);

        setQueryParams(query, params);
        applyPagination(query, filter);

        return query.getResultList();
    }

    private void appendNameFilterClause(StringBuilder whereClause, List<Object> params, AtomicInteger paramIndex, String nameFilter) {
        if (!StringUtils.isEmpty(nameFilter)) {
            String trimmedNameFilter = nameFilter.trim();
            if (!trimmedNameFilter.endsWith("%")) {
                trimmedNameFilter += "%";
            }
            params.add(paramIndex.get(), trimmedNameFilter);
            whereClause.append(" AND m.name like ?").append(paramIndex.incrementAndGet());
        }
    }

    private void appendSizeFilterClause(StringBuilder whereClause, List<Object> params, AtomicInteger paramIndex, MediaFileFilter filter) {
        if (filter.getSize() > 0) {
            params.add(paramIndex.get(), filter.getSize());
            whereClause.append(" AND m.length ").append(getSizeOperator(filter.getSizeFilterType()));
            whereClause.append(" ?").append(paramIndex.incrementAndGet());
        }
    }

    private String getSizeOperator(MediaFileFilter.SizeFilterType type) {
        switch (type) {
            case GT: return ">";
            case GTE: return ">=";
            case EQ: return "=";
            case LT: return "<";
            case LTE: return "<=";
            default: return "=";
        }
    }

    private void appendTagsFilterClause(StringBuilder whereClause, List<Object> params, AtomicInteger paramIndex, MediaFileFilter filter) {
        List<String> tags = filter.getTags();
        if (tags != null && !tags.isEmpty()) {
            if (tags.size() > 1) {
                whereClause.append(" AND EXISTS (SELECT t FROM MediaFileTag t WHERE t.mediaFile = m and t.name IN (");
                for (String tag : tags) {
                    params.add(paramIndex.get(), tag);
                    whereClause.append("?").append(paramIndex.incrementAndGet()).append(",");
                }
                whereClause.deleteCharAt(whereClause.lastIndexOf(","));
                whereClause.append("))");
            } else { // tags.size() == 1
                params.add(paramIndex.get(), tags.get(0));
                whereClause.append(" AND EXISTS (SELECT t FROM MediaFileTag t WHERE t.mediaFile = m and t.name = ?")
                        .append(paramIndex.incrementAndGet()).append(")");
            }
        }
    }

    private void appendTypeFilterClause(StringBuilder whereClause, List<Object> params, AtomicInteger paramIndex, MediaFileFilter filter) {
        MediaFileType type = filter.getType();
        if (type != null) {
            if (type == MediaFileType.OTHERS) {
                for (MediaFileType otherType : MediaFileType.values()) {
                    if (otherType != MediaFileType.OTHERS) {
                        params.add(paramIndex.get(), otherType.getContentTypePrefix() + "%");
                        whereClause.append(" AND m.contentType not like ?").append(paramIndex.incrementAndGet());
                    }
                }
            } else {
                params.add(paramIndex.get(), type.getContentTypePrefix() + "%");
                whereClause.append(" AND m.contentType like ?").append(paramIndex.incrementAndGet());
            }
        }
    }

    private String buildOrderByClause(MediaFileFilter filter) {
        StringBuilder orderBy = new StringBuilder();
        if (filter.getOrder() != null) {
            switch (filter.getOrder()) {
                case NAME: orderBy.append(" order by m.name"); break;
                case DATE_UPLOADED: orderBy.append(" order by m.dateUploaded"); break;
                case TYPE: orderBy.append(" order by m.contentType"); break;
                default: // No default action specified in original
            }
        } else {
            orderBy.append(" order by m.name"); // Default order
        }
        return orderBy.toString();
    }

    private void setQueryParams(TypedQuery<MediaFile> query, List<Object> params) {
        for (int i = 0; i < params.size(); i++) {
            query.setParameter(i + 1, params.get(i));
        }
    }

    private void applyPagination(TypedQuery<MediaFile> query,

                    } else {
                        // need to create a new mediafile directory
                        MediaFileDirectory secondDir = null;
                        try {
                            secondDir = new MediaFileDirectory(weblog, file.getName(), null);
                            roller.getMediaFileManager().createMediaFileDirectory(secondDir);
                            roller.flush();
                            dirCount++;
                        } catch (WebloggerException ex) {
                            log.error("ERROR creating directory: "
                                    + newDir.getName() + "/" + file.getName());
                        }
                        upgradeUploadsDir(weblog, user, file, secondDir);
                    }

                } else {
                    // a file: create a database record for it
                    // check to make sure that file does not already exist
                    if (newDir.hasMediaFile(file.getName())) {
                        log.debug("    Skipping file that already exists: "
                                + file.getName());

                    } else {

                        String originalPath = "/" + newDir.getName() + "/" + file.getName();
                        log.debug("Upgrade file with original path: " + originalPath);

                        MediaFile mf = new MediaFile();
                        try {
                            mf.setName(file.getName());
                            mf.setDescription(file.getName());
                            mf.setOriginalPath(originalPath);

                            mf.setDateUploaded(new Timestamp(file
                                    .lastModified()));
                            mf.setLastUpdated(new Timestamp(file.lastModified()));

                            mf.setDirectory(newDir);
                            mf.setWeblog(weblog);
                            mf.setCreatorUserName(user.getUserName());
                            mf.setSharedForGallery(Boolean.FALSE);

                            mf.setLength(file.length());
                            mf.setInputStream(new FileInputStream(file));
                            mf.setContentType(Utilities
                                    .getContentTypeFromFileName(file.getName()));

                            // Create
                            this.roller.getMediaFileManager().createMediaFile(
                                    weblog, mf, messages);
                            newDir.getMediaFiles().add(mf);

                            log.info(messages.toString());

                            fileCount++;

                        } catch (WebloggerException ex) {
                            log.error("ERROR writing file to new storage system: "
                                    + file.getAbsolutePath(), ex);

                        } catch (java.io.FileNotFoundException ex) {
                            log.error(
                                    "ERROR reading file from old storage system: "
                                            + file.getAbsolutePath(), ex);
                        }
                    }
                }
            }
        }

        try {
            // flush changes to this directory
chosenUser,
                                            new File(oldDirName + FS
                                                    + dir.getName()), root);

                                } catch (Exception e) {
                                    log.error("ERROR upgading weblog", e);
                                }
                            }
                        }
                    }
                }

                Properties props = new Properties();
                props.setProperty("complete", "true");
                props.store(new FileOutputStream(oldDirName + File.separator
                        + MIGRATION_STATUS_FILENAME), "Migration is complete!");

            } catch (Exception ioex) {
                log.error("ERROR upgrading", ioex);
            }
        }
        msgs.add("Migration complete!");
        return msgs;
    }

    private void upgradeUploadsDir(Weblog weblog, User user, File oldDir,
            MediaFileDirectory newDir) {

        log.debug("Upgrading dir: " + oldDir.getAbsolutePath());
        if (newDir == null) {
            log.error("newDir cannot be null");
            return;
        }

        int dirCount = 0;
        int fileCount = 0;
        File[] files = oldDir.listFiles();
        if (files != null) {
            for (File file: files) {
                if (file.isDirectory()) {
                    dirCount += handleDirectoryUpgrade(weblog, user, file, newDir);
                } else {
                    fileCount += handleFileUpgrade(weblog, user, file, newDir);
                }
            }
        }

        try {
            roller.flush();

            log.debug("Count of dirs created: " + dirCount);
            log.debug("Count of files created: " + fileCount);

        } catch (WebloggerException ex) {
            log.error("ERROR flushing changes to dir: " + newDir.getName(), ex);
        }
    }

    private int handleDirectoryUpgrade(Weblog weblog, User user, File directory, MediaFileDirectory parentNewDir) {
        if (weblog.hasMediaFileDirectory(directory.getName())) {
            MediaFileDirectory existingDir = weblog.getMediaFileDirectory(directory.getName());
            upgradeUploadsDir(weblog, user, directory, existingDir);
            return 0;
        } else {
            return createAndUpgradeMediaFileDirectory(weblog, user, directory, parentNewDir);
        }
    }

    private int createAndUpgradeMediaFileDirectory(Weblog weblog, User user, File directory, MediaFileDirectory parentNewDir) {
        MediaFileDirectory secondDir = null;
        int createdDirCount = 0;
        try {
            secondDir = new MediaFileDirectory(weblog, directory.getName(), null);
            roller.getMediaFileManager().createMediaFileDirectory(secondDir);
            roller.flush();
            createdDirCount = 1;
        } catch (WebloggerException ex) {
            log.error("ERROR creating directory: " + parentNewDir.getName() + "/" + directory.getName(), ex);
        }
        
        if (secondDir != null) {
            upgradeUploadsDir(weblog, user, directory, secondDir);
        }
        return createdDirCount;
    }

    private int handleFileUpgrade(Weblog weblog, User user, File file, MediaFileDirectory newDir) {
        if (newDir.hasMediaFile(file.getName())) {
            log.debug("    Skipping file that already exists: " + file.getName());
            return 0;
        } else {
            return createMediaFileRecord(weblog, user, file, newDir);
        }
    }

    private int createMediaFileRecord(Weblog weblog, User user, File file, MediaFileDirectory newDir) {
        int createdFileCount = 0;
        String originalPath = "/" + newDir.getName() + "/" + file.getName();
        log.debug("Upgrade file with original path: " + originalPath);

        MediaFile mf = new MediaFile();
        RollerMessages messages = new RollerMessages();

        try (FileInputStream fis = new FileInputStream(file)) {
            mf.setName(file.getName());
            mf.setDescription(file.getName());
            mf.setOriginalPath(originalPath);

            mf.setDateUploaded(new Timestamp(file.lastModified()));
            mf.setLastUpdated(new Timestamp(file.lastModified()));

            mf.setDirectory(newDir);
            mf.setWeblog(weblog);
            mf.setCreatorUserName(user.getUserName());
            mf.setSharedForGallery(Boolean.FALSE);

            mf.setLength(file.length());
            mf.setInputStream(fis);
            mf.setContentType(Utilities.getContentTypeFromFileName(file.getName()));

            this.roller.getMediaFileManager().createMediaFile(weblog, mf, messages);
            newDir.getMediaFiles().add(mf);

            log.info(messages.toString());
            createdFileCount = 1;

        } catch (WebloggerException ex) {
            log.error("ERROR writing file to new storage system: " + file.getAbsolutePath(), ex);
        } catch (java.io.FileNotFoundException ex) {
            log.error("ERROR reading file from old storage system: " + file.getAbsolutePath(), ex);
        } catch (java.io.IOException ex) {
            log.error("ERROR processing file: " + file.getAbsolutePath(), ex);
        }
        return createdFileCount;
    }

    @Override
    public void removeAllFiles(Weblog website) throws WebloggerException {
        removeMediaFileDirectory(getDefaultMediaFileDirectory(website));
    }

    @Override
    public void removeMediaFileDirectory(MediaFileDirectory dir)
            throws WebloggerException {
        if (dir == null) {
            return;
        }
        FileContentManager cmgr = WebloggerFactory.getWeblogger()
                .getFileContentManager();
        Set<MediaFile> files = dir.getMediaFiles();
        for (MediaFile mf : files) {
            try {
                cmgr.deleteFile(dir.getWeblog(), mf.getId());
                // Now thumbnail
                cmgr.deleteFile(dir.getWeblog(), mf.getId() + "_sm");
            } catch (Exception e) {
                log.debug("File to be deleted already unavailable in the file store");
            }
            this.strategy.remove(mf);
        }

        dir.getWeblog().getMediaFileDirectories().remove(dir);

        // Contained media files
        roller.flush();

        this.strategy.remove(dir);

        // Refresh associated parent
        roller.flush();
    }

    @Override
    public void removeMediaFileTag(String name, MediaFile entry)
            throws WebloggerException {

        for (Iterator<MediaFileTag> it = entry.getTags().iterator(); it.hasNext();) {
            MediaFileTag tag = it.next();
            if (tag.getName().equals(name)) {
// Refresh it from database
                this.strategy.remove(tag);

                // Refresh it from the collection
                it.remove();
            }
        }
    }
}
        }
    }
}