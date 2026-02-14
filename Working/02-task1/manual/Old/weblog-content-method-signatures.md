# Weblog Content - Method Signatures (Top 40 files by method count)

This list focuses on the most method-heavy files to keep documentation manageable while deepening coverage.

## app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAMediaFileManagerImpl.java
- `protected JPAMediaFileManagerImpl(Weblogger roller,
            JPAPersistenceStrategy persistenceStrategy) {`
- `public void initialize() {`
- `public void release() {`
- `public void moveMediaFiles(Collection<MediaFile> mediaFiles,
            MediaFileDirectory targetDirectory) throws WebloggerException {`
- `for (MediaFile mediaFile : moved) {`
- `public void moveMediaFile(MediaFile mediaFile,
            MediaFileDirectory targetDirectory) throws WebloggerException {`
- `public void createMediaFileDirectory(MediaFileDirectory directory)
            throws WebloggerException {`
- `public MediaFileDirectory createMediaFileDirectory(Weblog weblog,
            String requestedName) throws WebloggerException {`
- `public MediaFileDirectory createDefaultMediaFileDirectory(Weblog weblog)
            throws WebloggerException {`
- `public void createMediaFile(Weblog weblog, MediaFile mediaFile,
            RollerMessages errors) throws WebloggerException {`
- `public void createThemeMediaFile(Weblog weblog, MediaFile mediaFile,
                                RollerMessages errors) throws WebloggerException {`
- `private void updateThumbnail(MediaFile mediaFile) {`
- `public void updateMediaFile(Weblog weblog, MediaFile mediaFile)
            throws WebloggerException {`
- `public void updateMediaFile(Weblog weblog, MediaFile mediaFile,
            InputStream is) throws WebloggerException {`
- `public MediaFile getMediaFile(String id) throws WebloggerException {`
- `public MediaFile getMediaFile(String id, boolean includeContent)
            throws WebloggerException {`
- `if (includeContent) {`
- `public MediaFileDirectory getMediaFileDirectoryByName(Weblog weblog,
            String name) throws WebloggerException {`
- `public MediaFile getMediaFileByPath(Weblog weblog, String path)
            throws WebloggerException {`
- `if (slash > 0) {`
- `if (slash != -1) {`
- `public MediaFile getMediaFileByOriginalPath(Weblog weblog, String origpath)
            throws WebloggerException {`
- `if (null == origpath) {`
- `public MediaFileDirectory getMediaFileDirectory(String id)
            throws WebloggerException {`
- `public MediaFileDirectory getDefaultMediaFileDirectory(Weblog weblog)
            throws WebloggerException {`
- `public List<MediaFileDirectory> getMediaFileDirectories(Weblog weblog)
            throws WebloggerException {`
- `public void removeMediaFile(Weblog weblog, MediaFile mediaFile)
            throws WebloggerException {`
- `public List<MediaFile> fetchRecentPublicMediaFiles(int length)
            throws WebloggerException {`
- `public List<MediaFile> searchMediaFiles(Weblog weblog,
            MediaFileFilter filter) throws WebloggerException {`
- `if (type != MediaFileType.OTHERS) {`
- `public boolean isFileStorageUpgradeRequired() {`
- `if (uploadsDirName != null) {`
- `public List<String> upgradeFileStorage() {`
- `if (oldDirName != null) {`
- `if (null != dirs) {`
- `for (File dir : dirs) {`
- `if (weblog != null) {`
- `for (User user : users) {`
- `if (root == null) {`
- `private void upgradeUploadsDir(Weblog weblog, User user, File oldDir,
            MediaFileDirectory newDir) {`
- `if (newDir == null) {`
- `if (files != null) {`
- `for (File file: files) {`
- `public void removeAllFiles(Weblog website) throws WebloggerException {`
- `public void removeMediaFileDirectory(MediaFileDirectory dir)
            throws WebloggerException {`
- `if (dir == null) {`
- `for (MediaFile mf : files) {`
- `public void removeMediaFileTag(String name, MediaFile entry)
            throws WebloggerException {`

## app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAUserManagerImpl.java
- `protected JPAUserManagerImpl(JPAPersistenceStrategy strat) {`
- `public void release() {`
- `public void saveUser(User user) throws WebloggerException {`
- `public void removeUser(User user) throws WebloggerException {`
- `for (WeblogPermission perm : perms) {`
- `public void addUser(User newUser) throws WebloggerException {`
- `if (newUser == null) {`
- `if (adminUser) {`
- `public User getUser(String id) throws WebloggerException {`
- `public User getUserByUserName(String userName) throws WebloggerException {`
- `public User getUserByOpenIdUrl(String openIdUrl) throws WebloggerException {`
- `if (openIdUrl == null) {`
- `public User getUserByUserName(String userName, Boolean enabled)
            throws WebloggerException {`
- `if (userName==null) {`
- `if (user != null) {`
- `if (enabled != null) {`
- `for (int i=0; i<params.length; i++) {`
- `if(user != null) {`
- `public List<User> getUsers(Boolean enabled, Date startDate, Date endDate,
            int offset, int length)
            throws WebloggerException {`
- `if (enabled != null) {`
- `if (startDate != null) {`
- `if (startDate != null) {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public List<User> getUsersStartingWith(String startsWith, Boolean enabled,
            int offset, int length) throws WebloggerException {`
- `if (enabled != null) {`
- `if (startsWith != null) {`
- `if (startsWith != null) {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public Map<String, Long> getUserNameLetterMap() throws WebloggerException {`
- `for (int i=0; i<26; i++) {`
- `public List<User> getUsersByLetter(char letter, int offset, int length)
            throws WebloggerException {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public long getUserCount() throws WebloggerException {`
- `public User getUserByActivationCode(String activationCode) throws WebloggerException {`
- `if (activationCode == null) {`
- `public boolean checkPermission(RollerPermission perm, User user) throws WebloggerException {`
- `if (perm instanceof WeblogPermission) {`
- `public WeblogPermission getWeblogPermission(Weblog weblog, User user) throws WebloggerException {`
- `public WeblogPermission getWeblogPermissionIncludingPending(Weblog weblog, User user) throws WebloggerException {`
- `public void grantWeblogPermission(Weblog weblog, User user, List<String> actions) throws WebloggerException {`
- `if (existingPerm != null) {`
- `public void grantWeblogPermissionPending(Weblog weblog, User user, List<String> actions) throws WebloggerException {`
- `if (existingPerm != null) {`
- `public void confirmWeblogPermission(Weblog weblog, User user) throws WebloggerException {`
- `public void declineWeblogPermission(Weblog weblog, User user) throws WebloggerException {`
- `public void revokeWeblogPermission(Weblog weblog, User user, List<String> actions) throws WebloggerException {`
- `public List<WeblogPermission> getWeblogPermissions(User user) throws WebloggerException {`
- `public List<WeblogPermission> getWeblogPermissions(Weblog weblog) throws WebloggerException {`
- `public List<WeblogPermission> getWeblogPermissionsIncludingPending(Weblog weblog) throws WebloggerException {`
- `public List<WeblogPermission> getPendingWeblogPermissions(User user) throws WebloggerException {`
- `public List<WeblogPermission> getPendingWeblogPermissions(Weblog weblog) throws WebloggerException {`
- `public boolean hasRole(String roleName, User user) throws WebloggerException {`
- `public List<String> getRoles(User user) throws WebloggerException {`
- `if (roles != null) {`
- `for (UserRole userRole : roles) {`
- `public void grantRole(String roleName, User user) throws WebloggerException {`
- `public void revokeRole(String roleName, User user) throws WebloggerException {`

## app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAWeblogEntryManagerImpl.java
- `protected JPAWeblogEntryManagerImpl(Weblogger roller, JPAPersistenceStrategy strategy) {`
- `public void saveWeblogCategory(WeblogCategory cat) throws WebloggerException {`
- `public void removeWeblogCategory(WeblogCategory cat)
    throws WebloggerException {`
- `public void moveWeblogCategoryContents(WeblogCategory srcCat,
            WeblogCategory destCat)
            throws WebloggerException {`
- `for (WeblogEntry entry : results) {`
- `public void saveComment(WeblogEntryComment comment) throws WebloggerException {`
- `public void removeComment(WeblogEntryComment comment) throws WebloggerException {`
- `public void saveWeblogEntry(WeblogEntry entry) throws WebloggerException {`
- `if (cat == null) {`
- `public void removeWeblogEntry(WeblogEntry entry) throws WebloggerException {`
- `for (WeblogEntryComment comment : comments) {`
- `private List<WeblogEntry> getNextPrevEntries(WeblogEntry current, String catName,
            String locale, int maxEntries, boolean next)
            throws WebloggerException {`
- `if (current == null) {`
- `if (next) {`
- `if (catName != null) {`
- `if (category != null) {`
- `if(locale != null) {`
- `if (next) {`
- `public List<WeblogCategory> getWeblogCategories(Weblog website)
    throws WebloggerException {`
- `if (website == null) {`
- `public List<WeblogEntry> getWeblogEntries(WeblogEntrySearchCriteria wesc) throws WebloggerException {`
- `if (i != 0) {`
- `if (cat != null) {`
- `public List<WeblogEntry> getWeblogEntriesPinnedToMain(Integer max)
    throws WebloggerException {`
- `if (max != null) {`
- `public void removeWeblogEntryAttribute(String name, WeblogEntry entry)
    throws WebloggerException {`
- `private void removeWeblogEntryTag(WeblogEntryTag tag) throws WebloggerException {`
- `public WeblogEntry getWeblogEntryByAnchor(Weblog website,
            String anchor) throws WebloggerException {`
- `if (website == null) {`
- `if (anchor == null) {`
- `if(entry != null) {`
- `if(entry != null) {`
- `public String createAnchor(WeblogEntry entry) throws WebloggerException {`
- `while (true) {`
- `if (count > 0) {`
- `public boolean isDuplicateWeblogCategoryName(WeblogCategory cat)
    throws WebloggerException {`
- `public boolean isWeblogCategoryInUse(WeblogCategory cat)
    throws WebloggerException {`
- `public List<WeblogEntryComment> getComments(CommentSearchCriteria csc) throws WebloggerException {`
- `public int removeMatchingComments(
            Weblog     weblog,
            WeblogEntry entry,
            String  searchString,
            Date    startDate,
            Date    endDate,
            ApprovalStatus status) throws WebloggerException {`
- `for (WeblogEntryComment comment : comments) {`
- `public WeblogCategory getWeblogCategory(String id)
    throws WebloggerException {`
- `public WeblogCategory getWeblogCategoryByName(Weblog weblog,
            String categoryName) throws WebloggerException {`
- `public WeblogEntryComment getComment(String id) throws WebloggerException {`
- `public WeblogEntry getWeblogEntry(String id) throws WebloggerException {`
- `public Map<Date, List<WeblogEntry>> getWeblogEntryObjectMap(WeblogEntrySearchCriteria wesc) throws WebloggerException {`
- `for (WeblogEntry entry : entries) {`
- `public Map<Date, String> getWeblogEntryStringMap(WeblogEntrySearchCriteria wesc) throws WebloggerException {`
- `for (WeblogEntry entry : entries) {`
- `public List<StatCount> getMostCommentedWeblogEntries(Weblog website,
            Date startDate, Date endDate, int offset,
            int length) throws WebloggerException {`
- `if (website != null) {`
- `if (startDate != null) {`
- `if (startDate != null) {`
- `if (queryResults != null) {`
- `for (Object obj : queryResults) {`
- `public WeblogEntry getNextEntry(WeblogEntry current,
            String catName, String locale) throws WebloggerException {`
- `public WeblogEntry getPreviousEntry(WeblogEntry current,
            String catName, String locale) throws WebloggerException {`
- `public void release() {`
- `public void applyCommentDefaultsToEntries(Weblog website)
    throws WebloggerException {`
- `public List<TagStat> getPopularTags(Weblog website, Date startDate, int offset, int limit)
    throws WebloggerException {`
- `if (website != null) {`
- `if (startDate != null) {`
- `if (startDate != null) {`
- `if (queryResults != null) {`
- `for (Object obj : queryResults) {`
- `for (TagStat t : results) {`
- `public List<TagStat> getTags(Weblog website, String sortBy,
            String startsWith, int offset, int limit) throws WebloggerException {`
- `if (website != null) {`
- `if (queryResults != null) {`
- `for (Object obj : queryResults) {`
- `if (sortByName) {`
- `public boolean getTagComboExists(List<String> tags, Weblog weblog) throws WebloggerException{`
- `if(weblog != null) {`
- `private void updateTagCount(String name, Weblog website, int amount)
    throws WebloggerException {`
- `if (amount == 0) {`
- `if (website == null) {`
- `if (weblogTagData == null && amount > 0) {`
- `if (siteTagData == null && amount > 0) {`
- `public WeblogHitCount getHitCount(String id) throws WebloggerException {`
- `public WeblogHitCount getHitCountByWeblog(Weblog weblog)
    throws WebloggerException {`
- `public List<WeblogHitCount> getHotWeblogs(int sinceDays, int offset, int length)
    throws WebloggerException {`
- `private static void setFirstMax( Query query, int offset, int length )  {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public static Date getStartDateNow(int sinceDays) {`
- `public void saveHitCount(WeblogHitCount hitCount) throws WebloggerException {`
- `public void removeHitCount(WeblogHitCount hitCount) throws WebloggerException {`
- `public void incrementHitCount(Weblog weblog, int amount)
    throws WebloggerException {`
- `if(amount == 0) {`
- `if(weblog == null) {`
- `if(hitCount == null && amount > 0) {`
- `public void resetAllHitCounts() throws WebloggerException {`
- `public void resetHitCount(Weblog weblog) throws WebloggerException {`
- `public long getCommentCount() throws WebloggerException {`
- `public long getCommentCount(Weblog website) throws WebloggerException {`
- `public long getEntryCount() throws WebloggerException {`
- `public long getEntryCount(Weblog website) throws WebloggerException {`
- `private static StringBuilder appendConjuctionToWhereclause(StringBuilder whereClause,
            String expression) {`

## app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAWeblogManagerImpl.java
- `protected JPAWeblogManagerImpl(Weblogger roller, JPAPersistenceStrategy strat) {`
- `public void release() {`
- `public void saveWeblog(Weblog weblog) throws WebloggerException {`
- `public void removeWeblog(Weblog weblog) throws WebloggerException {`
- `private void removeWeblogContents(Weblog weblog)
    throws  WebloggerException {`
- `for (WeblogEntryTag tagData : results) {`
- `for (Object obj : queueEntries) {`
- `for (AutoPing autoPing : autopings) {`
- `for (WeblogTemplate template : templates) {`
- `for (WeblogBookmarkFolder wbf : folders) {`
- `for (WeblogEntry entry : entries) {`
- `protected void updateTagAggregates(List<TagStat> tags) throws WebloggerException {`
- `for (TagStat stat : tags) {`
- `public void saveTemplate(WeblogTemplate template) throws WebloggerException {`
- `public void saveTemplateRendition(CustomTemplateRendition rendition) throws WebloggerException {`
- `public void removeTemplate(WeblogTemplate template) throws WebloggerException {`
- `public void addWeblog(Weblog newWeblog) throws WebloggerException {`
- `private void addWeblogContents(Weblog newWeblog)
    throws WebloggerException {`
- `if (cats != null) {`
- `for (String split : splitcats) {`
- `if (firstCat == null) {`
- `if (firstCat != null) {`
- `if (blogroll != null) {`
- `for (String splitItem : splitroll) {`
- `if (rollitems.length > 1) {`
- `public Weblog getWeblog(String id) throws WebloggerException {`
- `public Weblog getWeblogByHandle(String handle) throws WebloggerException {`
- `public Weblog getWeblogByHandle(String handle, Boolean visible) throws WebloggerException {`
- `if (handle == null) {`
- `if(blogID != null) {`
- `if (weblog != null) {`
- `if(weblog != null) {`
- `public List<Weblog> getWeblogs(
            Boolean enabled, Boolean active,
            Date startDate, Date endDate, int offset, int length) throws WebloggerException {`
- `if (startDate != null) {`
- `if (endDate != null) {`
- `if (enabled != null) {`
- `if (active != null) {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public List<Weblog> getUserWeblogs(User user, boolean enabledOnly) throws WebloggerException {`
- `if (user == null) {`
- `for (WeblogPermission perm : perms) {`
- `public List<User> getWeblogUsers(Weblog weblog, boolean enabledOnly) throws WebloggerException {`
- `for (WeblogPermission perm : perms) {`
- `if (user == null) {`
- `public WeblogTemplate getTemplate(String id) throws WebloggerException {`
- `public WeblogTemplate getTemplateByLink(Weblog weblog, String templateLink)
    throws WebloggerException {`
- `if (weblog == null) {`
- `if (templateLink == null) {`
- `public WeblogTemplate getTemplateByAction(Weblog weblog, ComponentType action)
            throws WebloggerException {`
- `if (weblog == null) {`
- `if (action == null) {`
- `public WeblogTemplate getTemplateByName(Weblog weblog, String templateName)
    throws WebloggerException {`
- `if (weblog == null) {`
- `if (templateName == null) {`
- `public List<WeblogTemplate> getTemplates(Weblog weblog) throws WebloggerException {`
- `if (weblog == null) {`
- `public Map<String, Long> getWeblogHandleLetterMap() throws WebloggerException {`
- `for (int i=0; i<26; i++) {`
- `public List<Weblog> getWeblogsByLetter(char letter, int offset, int length)
    throws WebloggerException {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `public List<StatCount> getMostCommentedWeblogs(Date startDate, Date endDate,
            int offset, int length)
            throws WebloggerException {`
- `if (endDate == null) {`
- `if (startDate != null) {`
- `if (offset != 0) {`
- `if (length != -1) {`
- `if (queryResults != null) {`
- `for (Object obj : queryResults) {`
- `public long getWeblogCount() throws WebloggerException {`
- `private boolean isAlphanumeric(String str) {`
- `if (str == null) {`

## app/src/main/java/org/apache/roller/weblogger/business/MediaFileManager.java
- (No method signatures matched by regex)

## app/src/main/java/org/apache/roller/weblogger/business/search/lucene/LuceneIndexManager.java
- `protected LuceneIndexManager(Weblogger roller) {`
- `public void initialize() throws InitializationException {`
- `if (this.searchEnabled) {`
- `synchronized(this) {`
- `if (inconsistentAtStartup) {`
- `public void rebuildWeblogIndex() throws WebloggerException {`
- `public void rebuildWeblogIndex(Weblog website) throws WebloggerException {`
- `public void removeWeblogIndex(Weblog website) throws WebloggerException {`
- `public void addEntryIndexOperation(WeblogEntry entry) throws WebloggerException {`
- `public void addEntryReIndexOperation(WeblogEntry entry) throws WebloggerException {`
- `public void removeEntryIndexOperation(WeblogEntry entry) throws WebloggerException {`
- `public SearchResultList search(
        String term,
        String weblogHandle,
        String category,
        String locale,
        int pageNum,
        int entryCount,
        URLStrategy urlStrategy) throws WebloggerException {`
- `if (weblogSpecific) {`
- `if (category != null) {`
- `if (locale != null) {`
- `public ReadWriteLock getReadWriteLock() {`
- `public boolean isInconsistentAtStartup() {`
- `public static final Analyzer getAnalyzer() {`
- `private static Analyzer instantiateAnalyzer() {`
- `private static Analyzer instantiateDefaultAnalyzer() {`
- `private void scheduleIndexOperation(final IndexOperation op) {`
- `if (this.searchEnabled) {`
- `private void executeIndexOperationNow(final IndexOperation op) {`
- `if (this.searchEnabled) {`
- `public synchronized void resetSharedReader() {`
- `public synchronized IndexReader getSharedIndexReader() {`
- `if (reader == null) {`
- `public Directory getIndexDirectory() {`
- `private boolean indexExists() {`
- `private void deleteIndex() {`
- `for (String file : files) {`
- `private void createIndex(Directory dir) {`
- `if (writer != null) {`
- `public void release() {`
- `public void shutdown() {`
- `if (reader != null) {`
- `static SearchResultList convertHitsToEntryList(
        ScoreDoc[] hits,
        SearchOperation search,
        int pageNum,
        int entryCount,
        String weblogHandle,
        boolean websiteSpecificSearch,
        URLStrategy urlStrategy)
        throws WebloggerException {`
- `if (offset >= hits.length) {`
- `if (offset + limit > hits.length) {`
- `for (int i = offset; i < offset + limit; i++) {`

## app/src/main/java/org/apache/roller/weblogger/business/themes/SharedThemeTemplate.java
- `public SharedThemeTemplate() {`
- `public SharedThemeTemplate(String id, ComponentType action, String name,
            String desc, String contents, String link, Date date, 
            boolean hidden, boolean navbar) {`
- `public String getId() {`
- `public void setId(String id) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getDescription() {`
- `public void setDescription(String description) {`
- `public String getContents() {`
- `public void setContents(String contents) {`
- `public Date getLastModified() {`
- `public void setLastModified(Date lastModified) {`
- `public String getLink() {`
- `public void setLink(String link) {`
- `public boolean isHidden() {`
- `public void setHidden(boolean isHidden) {`
- `public boolean isNavbar() {`
- `public void setNavbar(boolean navbar) {`
- `public String getOutputContentType() {`
- `public void setOutputContentType(String outputContentType) {`
- `public String toString() {`
- `public ComponentType getAction() {`
- `public void setAction(ComponentType action) {`
- `public String getType() {`
- `public TemplateRendition getTemplateRendition(RenditionType type) throws WebloggerException {`
- `public void setType(String type) {`
- `public void addTemplateRendition(TemplateRendition rendition){`

## app/src/main/java/org/apache/roller/weblogger/business/URLStrategy.java
- (No method signatures matched by regex)

## app/src/main/java/org/apache/roller/weblogger/business/UserManager.java
- (No method signatures matched by regex)

## app/src/main/java/org/apache/roller/weblogger/business/WeblogEntryManager.java
- (No method signatures matched by regex)

## app/src/main/java/org/apache/roller/weblogger/business/Weblogger.java
- (No method signatures matched by regex)

## app/src/main/java/org/apache/roller/weblogger/business/WebloggerImpl.java
- `protected WebloggerImpl(
        AutoPingManager      autoPingManager,
        BookmarkManager      bookmarkManager,
        IndexManager         indexManager,
        MediaFileManager     mediaFileManager,
        FileContentManager   fileContentManager,
        PingQueueManager     pingQueueManager,
        PingTargetManager    pingTargetManager,
        PluginManager        pluginManager,
        PropertiesManager    propertiesManager,
        ThemeManager         themeManager,
        ThreadManager        threadManager,
        UserManager          userManager,
        WeblogManager        weblogManager,
        WeblogEntryManager   weblogEntryManager,
        OAuthManager         oauthManager,
        FeedFetcher          feedFetcher,
        PlanetManager        planetManager,
        org.apache.roller.planet.business.PlanetURLStrategy planetUrlStrategy,
        URLStrategy          urlStrategy) throws WebloggerException {`
- `public ThreadManager getThreadManager() {`
- `public IndexManager getIndexManager() {`
- `public ThemeManager getThemeManager() {`
- `public UserManager getUserManager() {`
- `public BookmarkManager getBookmarkManager() {`
- `public MediaFileManager getMediaFileManager() {`
- `public FileContentManager getFileContentManager() {`
- `public WeblogEntryManager getWeblogEntryManager() {`
- `public WeblogManager getWeblogManager() {`
- `public PropertiesManager getPropertiesManager() {`
- `public PingQueueManager getPingQueueManager() {`
- `public AutoPingManager getAutopingManager() {`
- `public PingTargetManager getPingTargetManager() {`
- `public PluginManager getPluginManager() {`
- `public OAuthManager getOAuthManager() {`
- `public URLStrategy getUrlStrategy() {`
- `public FeedFetcher getFeedFetcher() {`
- `public PlanetManager getPlanetManager() {`
- `public org.apache.roller.planet.business.PlanetURLStrategy getPlanetURLStrategy() {`
- `public void release() {`
- `public void initialize() throws InitializationException {`
- `public void shutdown() {`
- `if (indexManager != null) {`
- `if (threadManager != null) {`
- `public String getVersion() {`
- `public String getRevision() {`
- `public String getBuildTime() {`
- `public String getBuildUser() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/MediaFile.java
- `public MediaFile() {`
- `public String getId() {`
- `public void setId(String id) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getDescription() {`
- `public void setDescription(String description) {`
- `public String getCopyrightText() {`
- `public void setCopyrightText(String copyrightText) {`
- `public Boolean getSharedForGallery() {`
- `public void setSharedForGallery(Boolean isSharedForGallery) {`
- `public long getLength() {`
- `public void setLength(long length) {`
- `public Timestamp getDateUploaded() {`
- `public void setDateUploaded(Timestamp dateUploaded) {`
- `public long getLastModified() {`
- `public Timestamp getLastUpdated() {`
- `public void setLastUpdated(Timestamp time) {`
- `public MediaFileDirectory getDirectory() {`
- `public void setDirectory(MediaFileDirectory dir) {`
- `public Set<MediaFileTag> getTags() {`
- `private void setTags(Set<MediaFileTag> tagSet) throws WebloggerException {`
- `public void addTag(String name) throws WebloggerException {`
- `public void onRemoveTag(String name) throws WebloggerException {`
- `public Set<String> getAddedTags() {`
- `public Set<String> getRemovedTags() {`
- `public void updateTags(List<String> updatedTags) throws WebloggerException {`
- `if (updatedTags == null) {`
- `for (String inName : updatedTags) {`
- `for (String tag : removeTags) {`
- `for (String tag : newTags) {`
- `public String getTagsAsString() {`
- `public void setTagsAsString(String tags) throws WebloggerException {`
- `if (tags == null) {`
- `public String getContentType() {`
- `public void setContentType(String contentType) {`
- `public String getPath() {`
- `public InputStream getInputStream() {`
- `if (is != null) {`
- `public void setInputStream(InputStream is) {`
- `public void setContent(FileContent content) {`
- `public boolean isImageFile() {`
- `public String getPermalink() {`
- `public String getThumbnailURL() {`
- `public String getCreatorUserName() {`
- `public void setCreatorUserName(String creatorUserName) {`
- `public User getCreator() {`
- `public String getOriginalPath() {`
- `public void setOriginalPath(String originalPath) {`
- `public Weblog getWeblog() {`
- `public void setWeblog(Weblog weblog) {`
- `public int getWidth() {`
- `public void setWidth(int width) {`
- `public int getHeight() {`
- `public void setHeight(int height) {`
- `public InputStream getThumbnailInputStream() {`
- `if (thumbnail != null) {`
- `public void setThumbnailContent(FileContent thumbnail) {`
- `public int getThumbnailHeight() {`
- `public int getThumbnailWidth() {`
- `private void figureThumbnailSize() {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/StaticThemeTemplate.java
- `public StaticThemeTemplate(String id, TemplateLanguage lang) {`
- `public String getId() {`
- `public void setId(String id) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getDescription() {`
- `public void setDescription(String description) {`
- `public Date getLastModified() {`
- `public void setLastModified(Date lastModified) {`
- `public TemplateLanguage getTemplateLanguage() {`
- `public void setTemplateLanguage(TemplateLanguage templateLanguage) {`
- `public String getOutputContentType() {`
- `public RenditionType getType() {`
- `public TemplateRendition getTemplateRendition(RenditionType type) throws WebloggerException {`
- `public void setType(RenditionType type){`
- `public void setOutputContentType(String outputContentType) {`
- `public ComponentType getAction() {`
- `public void setAction(ComponentType action) {`
- `public String getLink() {`
- `public void setLink(String link) {`
- `public boolean isHidden() {`
- `public void setHidden(boolean hidden) {`
- `public boolean isNavbar() {`
- `public void setNavbar(boolean navbar) {`
- `public String getContents() {`
- `public void setContents(String contents) {`

## app/src/main/java/org/apache/roller/weblogger/pojos/User.java
- `public User() {`
- `public User( String id, String userName,
            String password, String fullName,
            String emailAddress,
            String locale, String timeZone,
            Date dateCreated,
            Boolean isEnabled) {`
- `public String getId() {`
- `public void setId( String id ) {`
- `public String getUserName() {`
- `public void setUserName( String userName ) {`
- `public String getPassword() {`
- `public void setPassword( String password ) {`
- `public void resetPassword(String newPassword) {`
- `public String getOpenIdUrl() {`
- `public void setOpenIdUrl(String openIdUrl) {`
- `public String getScreenName() {`
- `public void setScreenName( String screenName ) {`
- `public String getFullName() {`
- `public void setFullName( String fullName ) {`
- `public String getEmailAddress() {`
- `public void setEmailAddress( String emailAddress ) {`
- `public Date getDateCreated() {`
- `if (dateCreated == null) {`
- `public void setDateCreated(final Date date) {`
- `if (date != null) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public String getTimeZone() {`
- `public void setTimeZone(String timeZone) {`
- `public Boolean getEnabled() {`
- `public void setEnabled(Boolean enabled) {`
- `public String getActivationCode() {`
- `public void setActivationCode(String activationCode) {`
- `public boolean hasGlobalPermission(String action) {`
- `public boolean hasGlobalPermissions(List<String> actions) {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/Weblog.java
- `public Weblog() {`
- `public Weblog(
            String handle,
            String creator,
            String name,
            String desc,
            String email,
            String editorTheme,
            String locale,
            String timeZone) {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`
- `public WeblogTheme getTheme() {`
- `public String getId() {`
- `public void setId(String id) {`
- `public String getHandle() {`
- `public void setHandle(String handle) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getTagline() {`
- `public void setTagline(String tagline) {`
- `public org.apache.roller.weblogger.pojos.User getCreator() {`
- `public String getCreatorUserName() {`
- `public void setCreatorUserName(String creatorUserName) {`
- `public Boolean getEnableBloggerApi() {`
- `public void setEnableBloggerApi(Boolean enableBloggerApi) {`
- `public WeblogCategory getBloggerCategory() {`
- `public void setBloggerCategory(WeblogCategory bloggerCategory) {`
- `public String getEditorPage() {`
- `public void setEditorPage(String editorPage) {`
- `public String getBannedwordslist() {`
- `public void setBannedwordslist(String bannedwordslist) {`
- `public Boolean getAllowComments() {`
- `public void setAllowComments(Boolean allowComments) {`
- `public Boolean getDefaultAllowComments() {`
- `public void setDefaultAllowComments(Boolean defaultAllowComments) {`
- `public int getDefaultCommentDays() {`
- `public void setDefaultCommentDays(int defaultCommentDays) {`
- `public Boolean getModerateComments() {`
- `public void setModerateComments(Boolean moderateComments) {`
- `public Boolean getEmailComments() {`
- `public void setEmailComments(Boolean emailComments) {`
- `public String getEmailAddress() {`
- `public void setEmailAddress(String emailAddress) {`
- `public String getEditorTheme() {`
- `public void setEditorTheme(String editorTheme) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public String getTimeZone() {`
- `public void setTimeZone(String timeZone) {`
- `public Date getDateCreated() {`
- `if (dateCreated == null) {`
- `public void setDateCreated(final Date date) {`
- `if (date != null) {`
- `public String getDefaultPlugins() {`
- `public void setDefaultPlugins(String string) {`
- `public void setData(Weblog other) {`
- `public Locale getLocaleInstance() {`
- `public TimeZone getTimeZoneInstance() {`
- `public boolean hasUserPermission(User user, String action) {`
- `public boolean hasUserPermissions(User user, List<String> actions) {`
- `public int getEntryDisplayCount() {`
- `public void setEntryDisplayCount(int entryDisplayCount) {`
- `public Boolean getVisible() {`
- `public void setVisible(Boolean visible) {`
- `public Boolean getActive() {`
- `public void setActive(Boolean active) {`
- `public boolean getCommentModerationRequired() {`
- `public void setCommentModerationRequired(boolean modRequired) {`
- `public Date getLastModified() {`
- `public void setLastModified(Date lastModified) {`
- `public boolean isEnableMultiLang() {`
- `public void setEnableMultiLang(boolean enableMultiLang) {`
- `public boolean isShowAllLangs() {`
- `public void setShowAllLangs(boolean showAllLangs) {`
- `public String getURL() {`
- `public String getAbsoluteURL() {`
- `public String getIconPath() {`
- `public void setIconPath(String iconPath) {`
- `public String getAnalyticsCode() {`
- `public void setAnalyticsCode(String analyticsCode) {`
- `public String getAbout() {`
- `public void setAbout(String about) {`
- `public Map<String, WeblogEntryPlugin> getInitializedPlugins() {`
- `if (initializedPlugins == null) {`
- `public WeblogEntry getWeblogEntry(String anchor) {`
- `public WeblogCategory getWeblogCategory(String categoryName) {`
- `public List<WeblogEntry> getRecentWeblogEntries(String cat, int length) {`
- `if (length > MAX_ENTRIES) {`
- `if (length < 1) {`
- `public List<WeblogEntry> getRecentWeblogEntriesByTag(String tag, int length) {`
- `if (length > MAX_ENTRIES) {`
- `if (length < 1) {`
- `if (tag != null) {`
- `public List<WeblogEntryComment> getRecentComments(int length) {`
- `if (length > MAX_ENTRIES) {`
- `if (length < 1) {`
- `public WeblogBookmarkFolder getBookmarkFolder(String folderName) {`
- `public int getTodaysHits() {`
- `public List<TagStat> getPopularTags(int sinceDays, int length) {`
- `if(sinceDays > 0) {`
- `public long getCommentCount() {`
- `public long getEntryCount() {`
- `public void addCategory(WeblogCategory category) {`
- `public List<WeblogCategory> getWeblogCategories() {`
- `public void setWeblogCategories(List<WeblogCategory> cats) {`
- `public boolean hasCategory(String name) {`
- `public List<WeblogBookmarkFolder> getBookmarkFolders() {`
- `public void setBookmarkFolders(List<WeblogBookmarkFolder> bookmarkFolders) {`
- `public List<MediaFileDirectory> getMediaFileDirectories() {`
- `public void setMediaFileDirectories(List<MediaFileDirectory> mediaFileDirectories) {`
- `public void addBookmarkFolder(WeblogBookmarkFolder folder) {`
- `public boolean hasBookmarkFolder(String name) {`
- `public boolean hasMediaFileDirectory(String name) {`
- `public MediaFileDirectory getMediaFileDirectory(String name) {`

## app/src/main/java/org/apache/roller/weblogger/pojos/WeblogBookmark.java
- `public WeblogBookmark() {`
- `public WeblogBookmark(
            WeblogBookmarkFolder parent,
            String name,
            String desc,
            String url,
            String feedUrl,
            String image) {`
- `public String getId() {`
- `public void setId(String id) {`
- `public void calculatePriority() {`
- `if (size == 1) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getDescription() {`
- `public void setDescription(String description) {`
- `public String getUrl() {`
- `public void setUrl(String url) {`
- `public java.lang.Integer getPriority() {`
- `public void setPriority(java.lang.Integer priority) {`
- `public String getImage() {`
- `public void setImage(String image) {`
- `public String getFeedUrl() {`
- `public void setFeedUrl(String feedUrl) {`
- `public org.apache.roller.weblogger.pojos.WeblogBookmarkFolder getFolder() {`
- `public void setFolder(org.apache.roller.weblogger.pojos.WeblogBookmarkFolder folder) {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`
- `public int compareTo(WeblogBookmark o) {`
- `public Weblog getWebsite() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java
- `public WeblogEntry() {`
- `public WeblogEntry(
            String id,
            WeblogCategory category,
            Weblog website,
            User creator,
            String title,
            String link,
            String text,
            String anchor,
            Timestamp pubTime,
            Timestamp updateTime,
            PubStatus status) {`
- `public WeblogEntry(WeblogEntry otherData) {`
- `public void setData(WeblogEntry other) {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`
- `public String getId() {`
- `public void setId(String id) {`
- `public WeblogCategory getCategory() {`
- `public void setCategory(WeblogCategory category) {`
- `public List<WeblogCategory> getCategories() {`
- `public Weblog getWebsite() {`
- `public void setWebsite(Weblog website) {`
- `public User getCreator() {`
- `public String getCreatorUserName() {`
- `public void setCreatorUserName(String creatorUserName) {`
- `public String getTitle() {`
- `public void setTitle(String title) {`
- `public String getSummary() {`
- `public void setSummary(String summary) {`
- `public String getSearchDescription() {`
- `public void setSearchDescription(String searchDescription) {`
- `public String getText() {`
- `public void setText(String text) {`
- `public String getContentType() {`
- `public void setContentType(String contentType) {`
- `public String getContentSrc() {`
- `public void setContentSrc(String contentSrc) {`
- `public String getAnchor() {`
- `public void setAnchor(String anchor) {`
- `public Set<WeblogEntryAttribute> getEntryAttributes() {`
- `public void setEntryAttributes(Set<WeblogEntryAttribute> atts) {`
- `public String findEntryAttribute(String name) {`
- `public void putEntryAttribute(String name, String value) throws Exception {`
- `if (att == null) {`
- `public Timestamp getPubTime() {`
- `public void setPubTime(Timestamp pubTime) {`
- `public Timestamp getUpdateTime() {`
- `public void setUpdateTime(Timestamp updateTime) {`
- `public PubStatus getStatus() {`
- `public void setStatus(PubStatus status) {`
- `public String getLink() {`
- `public void setLink(String link) {`
- `public String getPlugins() {`
- `public void setPlugins(String string) {`
- `public Boolean getAllowComments() {`
- `public void setAllowComments(Boolean allowComments) {`
- `public Integer getCommentDays() {`
- `public void setCommentDays(Integer commentDays) {`
- `public Boolean getRightToLeft() {`
- `public void setRightToLeft(Boolean rightToLeft) {`
- `public Boolean getPinnedToMain() {`
- `public void setPinnedToMain(Boolean pinnedToMain) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public Set<WeblogEntryTag> getTags() {`
- `public void setTags(Set<WeblogEntryTag> tagSet) throws WebloggerException {`
- `public void addTag(String name) throws WebloggerException {`
- `public Set<WeblogEntryTag> getAddedTags() {`
- `public Set<WeblogEntryTag> getRemovedTags() {`
- `public String getTagsAsString() {`
- `for (WeblogEntryTag entryTag : tmp) {`
- `public void setTagsAsString(String tags) throws WebloggerException {`
- `for (String name : updatedTags) {`
- `for (String newTag : newTags) {`
- `public boolean getCommentsStillAllowed() {`
- `if (inPubTime == null) {`
- `public void setCommentsStillAllowed(boolean ignored) {`
- `public String formatPubTime(String pattern) {`
- `public String formatUpdateTime(String pattern) {`
- `public List<WeblogEntryComment> getComments() {`
- `public List<WeblogEntryComment> getComments(boolean ignoreSpam, boolean approvedOnly) {`
- `public int getCommentCount() {`
- `public String getPermalink() {`
- `public String getPermaLink() {`
- `public String getCommentsLink() {`
- `public String getDisplayTitle() {`
- `public String getRss09xDescription() {`
- `public String getRss09xDescription(int maxLength) {`
- `protected String createAnchor() throws WebloggerException {`
- `public String createAnchorBase() {`
- `public void setPermalink(String string) {`
- `public void setPermaLink(String string) {`
- `public void setDisplayTitle(String string) {`
- `public void setRss09xDescription(String string) {`
- `public List<String> getPluginsList() {`
- `public boolean isDraft() {`
- `public boolean isPending() {`
- `public boolean isPublished() {`
- `public String getTransformedText() {`
- `public String getTransformedSummary() {`
- `public boolean hasWritePermissions(User user) throws WebloggerException {`
- `if (hasAdmin) {`
- `private String render(String str) {`
- `if (str != null && inPlugins != null) {`
- `public String displayContent(String readMoreLink) {`
- `public String getDisplayContent() {`
- `public Boolean getRefreshAggregates() {`
- `public void setRefreshAggregates(Boolean refreshAggregates) {`

## app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntryComment.java
- `public WeblogEntryComment() {`
- `public String getId() {`
- `public void setId(String id) {`
- `public WeblogEntry getWeblogEntry() {`
- `public void setWeblogEntry(WeblogEntry entry) {`
- `public String getName() {`
- `public void setName(String name) {`
- `public String getEmail() {`
- `public void setEmail(String email) {`
- `public String getUrl() {`
- `public void setUrl(String url) {`
- `public String getContent() {`
- `public void setContent(String content) {`
- `public Timestamp getPostTime() {`
- `public void setPostTime(Timestamp postTime) {`
- `public ApprovalStatus getStatus() {`
- `public void setStatus(ApprovalStatus status) {`
- `public Boolean getNotify() {`
- `public void setNotify(Boolean notify) {`
- `public String getRemoteHost() {`
- `public void setRemoteHost(String remoteHost) {`
- `public String getReferrer() {`
- `public void setReferrer(String referrer) {`
- `public String getUserAgent() {`
- `public void setUserAgent(String userAgent) {`
- `public String getPlugins() {`
- `public void setPlugins(String plugins) {`
- `public String getContentType() {`
- `public void setContentType(String contentType) {`
- `public Boolean getSpam() {`
- `public Boolean getPending() {`
- `public Boolean getApproved() {`
- `public String getTimestamp() {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntrySearchCriteria.java
- `public Weblog getWeblog() {`
- `public void setWeblog(Weblog weblog) {`
- `public User getUser() {`
- `public void setUser(User user) {`
- `public Date getStartDate() {`
- `public void setStartDate(Date startDate) {`
- `public Date getEndDate() {`
- `public void setEndDate(Date endDate) {`
- `public String getCatName() {`
- `public void setCatName(String catName) {`
- `public List<String> getTags() {`
- `public void setTags(List<String> tags) {`
- `public PubStatus getStatus() {`
- `public void setStatus(PubStatus status) {`
- `public String getText() {`
- `public void setText(String text) {`
- `public SortBy getSortBy() {`
- `public void setSortBy(SortBy sortBy) {`
- `public SortOrder getSortOrder() {`
- `public void setSortOrder(SortOrder sortOrder) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public int getOffset() {`
- `public void setOffset(int offset) {`
- `public int getMaxResults() {`
- `public void setMaxResults(int maxResults) {`

## app/src/main/java/org/apache/roller/weblogger/pojos/WeblogTemplate.java
- `public WeblogTemplate() {`
- `public String getId() {`
- `public void setId( String id ) {`
- `public Weblog getWeblog() {`
- `public void setWeblog( Weblog website ) {`
- `public ComponentType getAction() {`
- `public void setAction(ComponentType action) {`
- `public String getName() {`
- `public void setName( String name ) {`
- `public String getDescription() {`
- `public void setDescription( String description ) {`
- `public String getLink() {`
- `public void setLink( String link ) {`
- `public Date getLastModified() {`
- `public void setLastModified(final Date newtime ) {`
- `public boolean isNavbar() {`
- `public void setNavbar(boolean navbar) {`
- `public boolean isHidden() {`
- `public void setHidden(boolean isHidden) {`
- `public String getOutputContentType() {`
- `public void setOutputContentType(String outputContentType) {`
- `public boolean isRequired() {`
- `public boolean isCustom() {`
- `public List<CustomTemplateRendition> getTemplateRenditions() {`
- `public void setTemplateRenditions(List<CustomTemplateRendition> templateRenditions) {`
- `public CustomTemplateRendition getTemplateRendition(CustomTemplateRendition.RenditionType desiredType) throws WebloggerException {`
- `for (CustomTemplateRendition rnd : templateRenditions) {`
- `public void addTemplateRendition(CustomTemplateRendition newRendition) {`
- `public boolean hasTemplateRendition(CustomTemplateRendition proposed) {`
- `for (CustomTemplateRendition rnd : templateRenditions) {`
- `public String toString() {`
- `public boolean equals(Object other) {`
- `if (other == this) {`
- `public int hashCode() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/wrapper/WeblogEntryWrapper.java
- `private WeblogEntryWrapper(WeblogEntry toWrap, URLStrategy strat) {`
- `public static WeblogEntryWrapper wrap(WeblogEntry toWrap, URLStrategy strat) {`
- `if(toWrap != null) {`
- `public String getId() {`
- `public WeblogCategoryWrapper getCategory() {`
- `public List<WeblogCategoryWrapper> getCategories() {`
- `public WeblogWrapper getWebsite() {`
- `public UserWrapper getCreator() {`
- `public String getTitle() {`
- `public String getSummary() {`
- `public String getText() {`
- `public String getContentType() {`
- `public String getContentSrc() {`
- `public String getAnchor() {`
- `public List<WeblogEntryAttributeWrapper> getEntryAttributes() {`
- `public String findEntryAttribute(String name) {`
- `public Timestamp getPubTime() {`
- `public Timestamp getUpdateTime() {`
- `public PubStatus getStatus() {`
- `public String getLink() {`
- `public String getPlugins() {`
- `public Boolean getAllowComments() {`
- `public Integer getCommentDays() {`
- `public Boolean getRightToLeft() {`
- `public Boolean getPinnedToMain() {`
- `public String getLocale() {`
- `public List<WeblogEntryTagWrapper> getTags() {`
- `public String getTagsAsString() {`
- `public boolean getCommentsStillAllowed() {`
- `public String formatPubTime(String pattern) {`
- `public String formatUpdateTime(String pattern) {`
- `public List<WeblogEntryCommentWrapper> getComments() {`
- `public List<WeblogEntryCommentWrapper> getComments(boolean ignoreSpam, boolean approvedOnly) {`
- `public int getCommentCount() {`
- `public String getPermalink() {`
- `public String getPermaLink() {`
- `public String getCommentsLink() {`
- `public String getDisplayTitle() {`
- `public String getRss09xDescription() {`
- `public String getRss09xDescription(int maxLength) {`
- `public List<String> getPluginsList() {`
- `public String getTransformedText() {`
- `public String getTransformedSummary() {`
- `public String displayContent(String readMoreLink) {`
- `public String getDisplayContent() {`
- `public String getSearchDescription() {`
- `public WeblogEntry getPojo() {`

## app/src/main/java/org/apache/roller/weblogger/pojos/wrapper/WeblogWrapper.java
- `private WeblogWrapper(Weblog toWrap, URLStrategy strat) {`
- `public static WeblogWrapper wrap(Weblog toWrap, URLStrategy strat) {`
- `if (toWrap != null) {`
- `public ThemeTemplateWrapper getTemplateByAction(ComponentType action) throws WebloggerException {`
- `public ThemeTemplateWrapper getTemplateByName(String name) throws WebloggerException {`
- `public ThemeTemplateWrapper getTemplateByLink(String link) throws WebloggerException {`
- `public List<ThemeTemplateWrapper> getTemplates() throws WebloggerException {`
- `public String getId() {`
- `public String getHandle() {`
- `public String getName() {`
- `public String getTagline() {`
- `public UserWrapper getCreator() {`
- `public Boolean getEnableBloggerApi() {`
- `public WeblogCategoryWrapper getBloggerCategory() {`
- `public String getEditorPage() {`
- `public String getBannedwordslist() {`
- `public Boolean getAllowComments() {`
- `public Boolean getDefaultAllowComments() {`
- `public int getDefaultCommentDays() {`
- `public Boolean getModerateComments() {`
- `public String getAnalyticsCode() {`
- `public Boolean getEmailComments() {`
- `public String getEmailAddress() {`
- `public String getEditorTheme() {`
- `public String getLocale() {`
- `public String getTimeZone() {`
- `public Date getDateCreated() {`
- `public String getDefaultPlugins() {`
- `public Locale getLocaleInstance() {`
- `public TimeZone getTimeZoneInstance() {`
- `public int getEntryDisplayCount() {`
- `public Boolean getVisible() {`
- `public Boolean getEnabled() {`
- `public Boolean getActive() {`
- `public Date getLastModified() {`
- `public boolean isEnableMultiLang() {`
- `public boolean isShowAllLangs() {`
- `public String getStylesheet() throws WebloggerException {`
- `public String getIcon() {`
- `if(iconPath == null) {`
- `public String getAbout() {`
- `public String getURL() {`
- `public String getAbsoluteURL() {`
- `public WeblogEntryWrapper getWeblogEntry(String anchor) {`
- `public List<WeblogCategoryWrapper> getWeblogCategories() {`
- `public WeblogCategoryWrapper getWeblogCategory(String categoryName) {`
- `public List<WeblogEntryWrapper> getRecentWeblogEntries(String cat, int length) {`
- `public List<WeblogEntryWrapper> getRecentWeblogEntriesByTag(String tag, int length) {`
- `public List<WeblogEntryCommentWrapper> getRecentComments(int length) {`
- `public WeblogBookmarkFolderWrapper getBookmarkFolder(String folderName) {`
- `public int getTodaysHits() {`
- `public List<TagStat> getPopularTags(int sinceDays,int length) {`
- `public long getCommentCount() {`
- `public long getEntryCount() {`
- `public Weblog getPojo() {`

## app/src/main/java/org/apache/roller/weblogger/ui/rendering/model/ConfigModel.java
- `public String getModelName() {`
- `public void init(Map<String, Object> map) throws WebloggerException {`
- `public String getSiteName() {`
- `public String getSiteShortName() {`
- `public String getSiteDescription() {`
- `public String getSiteEmail() {`
- `public boolean getRegistrationEnabled() {`
- `public String getRegistrationURL() {`
- `public boolean getFeedHistoryEnabled() {`
- `public int getFeedSize() {`
- `public int getFeedMaxSize() {`
- `public boolean getFeedStyle() {`
- `public boolean getCommentHtmlAllowed() {`
- `public boolean getCommentAutoFormat() {`
- `public boolean getCommentEscapeHtml() {`
- `public boolean getCommentEmailNotify() {`
- `public boolean getTrackbacksEnabled() {`
- `public String getRollerVersion() {`
- `public String getRollerBuildTimestamp() {`
- `public String getRollerBuildUser() {`
- `public String getDefaultAnalyticsTrackingCode() {`
- `public boolean getAnalyticsOverrideAllowed() {`
- `private String getProperty(String name) {`
- `private int getIntProperty(String name) {`
- `private boolean getBooleanProperty(String name) {`

## app/src/main/java/org/apache/roller/weblogger/ui/rendering/model/SiteModel.java
- `public String getModelName() {`
- `public void init(Map<String, Object> initData) throws WebloggerException {`
- `if(this.weblogRequest == null) {`
- `if (weblogRequest instanceof WeblogPageRequest) {`
- `if(urlStrategy == null) {`
- `public Pager<WeblogEntryWrapper> getWeblogEntriesPager(int sinceDays, int length) {`
- `if (feedRequest != null) {`
- `public Pager<WeblogEntryWrapper> getWeblogEntriesPager(WeblogWrapper queryWeblog, int sinceDays, int length) {`
- `public Pager<WeblogEntryWrapper> getWeblogEntriesPager(WeblogWrapper queryWeblog, User user, int sinceDays, int length) {`
- `public Pager<WeblogEntryWrapper> getWeblogEntriesPager(WeblogWrapper queryWeblog, User user, String cat, int sinceDays, int length) {`
- `if (feedRequest != null) {`
- `public Pager<WeblogEntryCommentWrapper> getCommentsPager(int sinceDays, int length) {`
- `if (feedRequest != null) {`
- `public Pager<UserWrapper> getUsersByLetterPager(String letter, int sinceDays, int length) {`
- `if (feedRequest != null) {`
- `public Pager<WeblogWrapper> getWeblogsByLetterPager(String letter, int sinceDays, int length) {`
- `public Map<String, Long> getUserNameLetterMap() {`
- `public Map<String, Long> getWeblogHandleLetterMap() {`
- `public List<WeblogWrapper> getUsersWeblogs(String userName) {`
- `for (WeblogPermission perm : perms) {`
- `public List<UserWrapper> getWeblogsUsers(String handle) {`
- `for (WeblogPermission perm : perms) {`
- `public UserWrapper getUser(String username) {`
- `public WeblogWrapper getWeblog(String handle) {`
- `public List<WeblogWrapper> getNewWeblogs(int sinceDays, int length) {`
- `for (Weblog website : weblogs) {`
- `public List<UserWrapper> getNewUsers(int sinceDays, int length) {`
- `for (User user : users) {`
- `public List<StatCount> getHotWeblogs(int sinceDays, int length) {`
- `for (WeblogHitCount hitCount : hotBlogs) {`
- `public List<StatCount> getMostCommentedWeblogs(int sinceDays , int length) {`
- `public List<StatCount> getMostCommentedWeblogEntries(List<String> cats, int sinceDays, int length) {`
- `public List<WeblogEntryWrapper> getPinnedWeblogEntries(int length) {`
- `for (WeblogEntry entry : weblogEntries) {`
- `public List<TagStat> getPopularTags(int sinceDays, int length) {`
- `if(sinceDays > 0) {`
- `public long getCommentCount() {`
- `public long getEntryCount() {`
- `public long getWeblogCount() {`
- `public long getUserCount() {`

## app/src/main/java/org/apache/roller/weblogger/ui/rendering/model/URLModel.java
- `public URLModel() {`
- `public String getModelName() {`
- `public void init(Map<String, Object> initData) throws WebloggerException {`
- `if(weblogRequest == null) {`
- `if(urlStrategy == null) {`
- `public String getSite() {`
- `public String getAbsoluteSite() {`
- `if (weblogAbsoluteURL != null) {`
- `public String getLogin() {`
- `public String getLogout() {`
- `public String getRegister() {`
- `public String action(String action, String namespace) {`
- `if(namespace != null) {`
- `public String getCommentAuthenticator() {`
- `public String themeResource(String theme, String filePath) {`
- `public String themeResource(String theme, String filePath, boolean absolute) {`
- `if (absolute) {`
- `public String getHome() {`
- `public String home(int pageNum) {`
- `public String home(String customLocale) {`
- `public String home(String customLocale, int pageNum) {`
- `public String entry(String anchor) {`
- `public String comment(String anchor, String timeStamp) {`
- `public String comments(String anchor) {`
- `public String trackback(String anchor) {`
- `public String date(String dateString) {`
- `public String date(String dateString, int pageNum) {`
- `public String category(String catName) {`
- `public String category(String catName, int pageNum) {`
- `public String tag(String tag) {`
- `public String tag(String tag, int pageNum) {`
- `public String tags(List<String> tags) {`
- `public String tags(List<String> tags, int pageNum) {`
- `public String collection(String dateString, String catName) {`
- `public String collection(String dateString, String catName, int pageNum) {`
- `public String getSearch() {`
- `public String search(String query, int pageNum) {`
- `public String search(String query, String catName, int pageNum) {`
- `public String absoluteSearch(String query, String catName, int pageNum) {`
- `public String getOpenSearchSite() {`
- `public String getOpenSearchWeblog() {`
- `public String page(String pageLink) {`
- `public String page(String pageLink, String dateString, String catName, int pageNum) {`
- `public String resource(String filePath) {`
- `public String getRsd() {`
- `public FeedURLS getFeed() {`
- `public String editEntry(String anchor) {`
- `if(entry != null) {`
- `public String getCreateEntry() {`
- `public String getEditSettings() {`
- `public EntryFeedURLS getEntries() {`
- `public CommentFeedURLS getComments() {`
- `public MediaFileFeedURLS getMediaFiles() {`
- `public String getRss() {`
- `public String rss(String catName, boolean excerpts) {`
- `public String rssByTags(List<String> tags, boolean excerpts) {`
- `public String getAtom() {`
- `public String atom(String catName, boolean excerpts) {`
- `public String search(String term, String catName) {`
- `public String atomByTags(List<String> tags, boolean excerpts) {`
- `public String getRss() {`
- `public String rss(String catName, boolean excerpts) {`
- `public String getAtom() {`
- `public String atom(String catName, boolean excerpts) {`
- `public String getRss() {`
- `public String rss(String catName, boolean excerpts) {`
- `public String getAtom() {`
- `public String atom(String catName, boolean excerpts) {`

## app/src/main/java/org/apache/roller/weblogger/ui/rendering/model/UtilitiesModel.java
- `public String getModelName() {`
- `public void init(Map<String, Object> initData) throws WebloggerException {`
- `if(parsedRequest == null) {`
- `if(parsedRequest instanceof WeblogRequest) {`
- `public boolean isUserAuthorizedToAuthor(WeblogWrapper weblog) {`
- `public boolean isUserAuthorizedToAdmin(WeblogWrapper weblog) {`
- `public boolean isUserAuthenticated() {`
- `public UserWrapper getAuthenticatedUser() {`
- `public static Date getNow() {`
- `public String formatDate(Date d, String fmt) {`
- `public String formatDate(Date d, String fmt, TimeZone tzOverride) {`
- `if (d == null || fmt == null) {`
- `if(tzOverride != null) {`
- `public String formatIso8601Date(Date d) {`
- `public String formatIso8601Day(Date d) {`
- `public String formatRfc822Date(Date date) {`
- `public String format8charsDate(Date date) {`
- `public boolean isEmpty(String str) {`
- `public boolean isNotEmpty(String str) {`
- `public String[] split(String str1, String str2) {`
- `public boolean equals(String str1, String str2) {`
- `public boolean isAlphanumeric(String str) {`
- `public String[] stripAll(String[] strs) {`
- `public String left(String str, int length) {`
- `public String escapeHTML(String str) {`
- `public String unescapeHTML(String str) {`
- `public String escapeXML(String str) {`
- `public String unescapeXML(String str) {`
- `public String escapeJavaScript(String str) {`
- `public String unescapeJavaScript(String str) {`
- `public String replace(String src, String target, String rWith) {`
- `public String replace(String src, String target, String rWith, int maxCount) {`
- `private String replace(String string, Pattern pattern, String replacement) {`
- `public String removeHTML(String str) {`
- `public String removeHTML(String str, boolean addSpace) {`
- `public String autoformat(String s) {`
- `public String truncate(String str, int lower, int upper, String appendToEnd) {`
- `public String truncateNicely(String str, int lower, int upper, String appendToEnd) {`
- `public String truncateText(String str, int lower, int upper, String appendToEnd) {`
- `public String hexEncode(String str) {`
- `public String encodeEmail(String str) {`
- `public final String encode(String s) {`
- `if(s != null) {`
- `public final String decode(String s) {`
- `if(s != null) {`
- `public String addNofollow(String html) {`
- `public String transformToHTMLSubset(String s) {`
- `public String toBase64(byte[] aValue) {`

## app/src/main/java/org/apache/roller/weblogger/ui/rendering/util/WeblogPageRequest.java
- `public WeblogPageRequest() {`
- `public WeblogPageRequest(HttpServletRequest request)
            throws InvalidRequestException {`
- `if (pathElements.length == 2) {`
- `if (tagsString != null) {`
- `if (pathInfo == null || this.weblogPageName != null) {`
- `if (this.weblogAnchor == null && this.tags == null) {`
- `boolean isValidDestination(String servlet) {`
- `private boolean isValidDateString(String dateString) {`
- `public String getContext() {`
- `public void setContext(String context) {`
- `public String getWeblogAnchor() {`
- `public void setWeblogAnchor(String weblogAnchor) {`
- `public String getWeblogPageName() {`
- `public void setWeblogPageName(String weblogPage) {`
- `public String getWeblogCategoryName() {`
- `public void setWeblogCategoryName(String weblogCategory) {`
- `public String getWeblogDate() {`
- `public void setWeblogDate(String weblogDate) {`
- `public int getPageNum() {`
- `public void setPageNum(int pageNum) {`
- `public Map<String, String[]> getCustomParams() {`
- `public void setCustomParams(Map<String, String[]> customParams) {`
- `public List<String> getTags() {`
- `public void setTags(List<String> tags) {`
- `public WeblogEntry getWeblogEntry() {`
- `if (weblogEntry == null && weblogAnchor != null) {`
- `public void setWeblogEntry(WeblogEntry weblogEntry) {`
- `public ThemeTemplate getWeblogPage() {`
- `if (weblogPage == null && weblogPageName != null) {`
- `public void setWeblogPage(WeblogTemplate weblogPage) {`
- `public WeblogCategory getWeblogCategory() {`
- `if (weblogCategory == null && weblogCategoryName != null) {`
- `public void setWeblogCategory(WeblogCategory weblogCategory) {`
- `public boolean isWebsitePageHit() {`
- `public void setWebsitePageHit(boolean websitePageHit) {`
- `public boolean isOtherPageHit() {`
- `public void setOtherPageHit(boolean otherPageHit) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/admin/CreateUserBean.java
- `public List<String> getList() {`
- `public void setList(List<String> list) {`
- `public String getId() {`
- `public void setId(String id) {`
- `public String getUserName() {`
- `public void setUserName(String userName) {`
- `public String getPassword() {`
- `public void setPassword(String password) {`
- `public String getScreenName() {`
- `public void setScreenName(String screenName) {`
- `public String getFullName() {`
- `public void setFullName(String fullName) {`
- `public String getEmailAddress() {`
- `public void setEmailAddress(String emailAddress) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public String getTimeZone() {`
- `public void setTimeZone(String timeZone) {`
- `public String getOpenIdUrl() {`
- `public void setOpenIdUrl(String openIdUrl) {`
- `public Boolean getEnabled() {`
- `public void setEnabled(Boolean enabled) {`
- `public String getActivationCode() {`
- `public void setActivationCode(String activationCode) {`
- `public boolean isAdministrator() {`
- `public void setAdministrator(boolean administrator) {`
- `public void copyTo(User dataHolder) {`
- `public void copyFrom(User dataHolder) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/core/ProfileBean.java
- `public String getId() {`
- `public void setId(String id) {`
- `public String getUserName() {`
- `public void setUserName(String userName) {`
- `public String getPassword() {`
- `public void setPassword(String password) {`
- `public String getScreenName() {`
- `public void setScreenName(String screenName) {`
- `public String getFullName() {`
- `public void setFullName(String fullName) {`
- `public String getEmailAddress() {`
- `public void setEmailAddress(String emailAddress) {`
- `public String getLocale() {`
- `public void setLocale(String locale) {`
- `public String getTimeZone() {`
- `public void setTimeZone(String timeZone) {`
- `public String getOpenIdUrl() {`
- `public void setOpenIdUrl(String openIdUrl) {`
- `public String getPasswordText() {`
- `public void setPasswordText(String passwordText) {`
- `public String getPasswordConfirm() {`
- `public void setPasswordConfirm(String passwordConfirm) {`
- `public void copyTo(User dataHolder) {`
- `public void copyFrom(User dataHolder) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/CommentsBean.java
- `public void loadCheckboxes(List<WeblogEntryComment> comments) {`
- `for (WeblogEntryComment comment : comments) {`
- `public ApprovalStatus getStatus() {`
- `public Date getStartDate() {`
- `public Date getEndDate() {`
- `public String getIds() {`
- `public void setIds(String ids) {`
- `public String getSearchString() {`
- `public void setSearchString(String searchString) {`
- `public String[] getApprovedComments() {`
- `public void setApprovedComments(String[] approvedComments) {`
- `public String[] getSpamComments() {`
- `public void setSpamComments(String[] spamComments) {`
- `public String[] getDeleteComments() {`
- `public void setDeleteComments(String[] deleteComments) {`
- `public String getApprovedString() {`
- `public void setApprovedString(String approvedString) {`
- `public int getPage() {`
- `public void setPage(int page) {`
- `public String getStartDateString() {`
- `public void setStartDateString(String startDateString) {`
- `public String getEndDateString() {`
- `public void setEndDateString(String endDateString) {`
- `public String getEntryId() {`
- `public void setEntryId(String entryId) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/EntryBean.java
- `public String getId() {`
- `public void setId( String id ) {`
- `public String getTitle() {`
- `public void setTitle( String title ) {`
- `public String getSummary() {`
- `public void setSummary( String summary ) {`
- `public String getText() {`
- `public void setText( String text ) {`
- `public String getStatus() {`
- `public void setStatus( String status ) {`
- `public String getLocale() {`
- `public void setLocale( String locale ) {`
- `public String getTagsAsString() {`
- `public void setTagsAsString( String tagsAsString ) {`
- `public String getCategoryId() {`
- `public void setCategoryId(String categoryId) {`
- `public String[] getPlugins() {`
- `public void setPlugins(String[] plugins ) {`
- `public String getDateString() {`
- `public void setDateString(String date) {`
- `public int getHours() {`
- `public void setHours(int hours) {`
- `public int getMinutes() {`
- `public void setMinutes(int minutes) {`
- `public int getSeconds() {`
- `public void setSeconds(int seconds) {`
- `public boolean getAllowComments() {`
- `public void setAllowComments( boolean allowComments ) {`
- `public Integer getCommentDays() {`
- `public void setCommentDays(Integer commentDays) {`
- `if (commentDays == -1) {`
- `public int getCommentCount() {`
- `public void setCommentCount(int commentCount) {`
- `public boolean getRightToLeft() {`
- `public void setRightToLeft( boolean rightToLeft ) {`
- `public boolean getPinnedToMain() {`
- `public void setPinnedToMain( boolean pinnedToMain ) {`
- `public String getEnclosureURL() {`
- `public void setEnclosureURL(String enclosureUrl) {`
- `public String getSearchDescription() {`
- `public void setSearchDescription(String searchDescription) {`
- `public Timestamp getPubTime(Locale locale, TimeZone timezone) {`
- `public boolean isDraft() {`
- `public boolean isPending() {`
- `public boolean isPublished() {`
- `public boolean isScheduled() {`
- `public void copyTo(WeblogEntry entry) throws WebloggerException {`
- `if(cat == null) {`
- `public void copyFrom(WeblogEntry entry, Locale locale) {`
- `for (WeblogEntryAttribute attr : attrs) {`
- `public String toString() {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/EntryEdit.java
- `public EntryEdit() {`
- `public void setPageTitle(String pageTitle) {`
- `public List<String> requiredWeblogPermissionActions() {`
- `public void myPrepare() {`
- `public String execute() {`
- `public String saveDraft() {`
- `public String publish() {`
- `private String save() {`
- `public EntryBean getBean() {`
- `public void setBean(EntryBean bean) {`
- `public WeblogEntry getEntry() {`
- `public void setEntry(WeblogEntry entry) {`
- `public String firstSave() {`
- `private void addStatusMessage(PubStatus pubStatus) {`
- `switch (pubStatus) {`
- `public String getPreviewURL() {`
- `public String getTrackbackUrl() {`
- `public void setTrackbackUrl(String trackbackUrl) {`
- `public String trackback() {`
- `if (results != null) {`
- `public List<WeblogCategory> getCategories() {`
- `public List<WeblogEntryPlugin> getEntryPlugins() {`
- `public WeblogEntryEditor getEditor() {`
- `public boolean isUserAnAuthor() {`
- `public String getJsonAutocompleteUrl() {`
- `public List<WeblogEntry> getRecentPublishedEntries() {`
- `public List<WeblogEntry> getRecentScheduledEntries() {`
- `public List<WeblogEntry> getRecentDraftEntries() {`
- `public List<WeblogEntry> getRecentPendingEntries() {`
- `private List<WeblogEntry> getRecentEntries(PubStatus pubStatus, WeblogEntrySearchCriteria.SortBy sortBy) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/MediaFileBean.java
- `public String getName() {`
- `public void setName(String name) {`
- `public String getDescription() {`
- `public void setDescription(String description) {`
- `public String getCopyrightText() {`
- `public void setCopyrightText(String copyrightText) {`
- `public String getTagsAsString() {`
- `public void setTagsAsString(String tagsAsString) {`
- `public String getDirectoryId() {`
- `public void setDirectoryId(String directoryId) {`
- `public boolean isSharedForGallery() {`
- `public void setSharedForGallery(boolean isSharedForGallery) {`
- `public String getId() {`
- `public void setId(String id) {`
- `public void copyTo(MediaFile dataHolder) throws WebloggerException {`
- `public void copyFrom(MediaFile dataHolder) {`
- `public String getPermalink() {`
- `public void setPermalink(String permalink) {`
- `public boolean isIsImage() {`
- `public void setIsImage(boolean isImage) {`
- `public String getThumbnailURL() {`
- `public void setThumbnailURL(String thumbnailURL) {`
- `public int getWidth() {`
- `public void setWidth(int width) {`
- `public int getHeight() {`
- `public void setHeight(int height) {`
- `public long getLength() {`
- `public void setLength(long length) {`
- `public String getContentType() {`
- `public void setContentType(String contentType) {`
- `public String getOriginalPath() {`
- `public void setOriginalPath(String originalPath) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/MediaFileView.java
- `public MediaFileView() {`
- `public void myPrepare() {`
- `if (SIZE_FILTER_TYPES == null) {`
- `public String createNewDirectory() {`
- `if (dirCreated) {`
- `public String fetchDirectoryContentLight() {`
- `public String execute() {`
- `if (directory != null) {`
- `public String view() {`
- `public String search() {`
- `if (valSuccess) {`
- `public String deleteSelected() {`
- `public String delete() {`
- `public String deleteFolder() {`
- `if (directoryId != null) {`
- `public String includeInGallery() {`
- `public String moveSelected() {`
- `public String getDirectoryId() {`
- `public void setDirectoryId(String id) {`
- `public List<MediaFile> getChildFiles() {`
- `public void setChildFiles(List<MediaFile> files) {`
- `public String getNewDirectoryName() {`
- `public void setNewDirectoryName(String newDirectoryName) {`
- `public MediaFileDirectory getCurrentDirectory() {`
- `public void setCurrentDirectory(MediaFileDirectory currentDirectory) {`
- `public String getDirectoryName() {`
- `public void setDirectoryName(String path) {`
- `public String getSortBy() {`
- `public void setSortBy(String sortBy) {`
- `public boolean myValidate() {`
- `public MediaFileSearchBean getBean() {`
- `public void setBean(MediaFileSearchBean b) {`
- `public List<KeyValueObject> getFileTypes() {`
- `public List<KeyValueObject> getSizeFilterTypes() {`
- `public List<KeyValueObject> getSizeUnits() {`
- `public List<KeyValueObject> getSortOptions() {`
- `public MediaFilePager getPager() {`
- `public void setPager(MediaFilePager pager) {`
- `public String getNewDirectoryPath() {`
- `public void setNewDirectoryPath(String newDirectoryPath) {`
- `public String getViewDirectoryId() {`
- `public void setViewDirectoryId(String viewDirectoryId) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/TemplateEditBean.java
- `public String getId() {`
- `public void setId( String id ) {`
- `public String getName() {`
- `public void setName( String name ) {`
- `public void setAction(ComponentType action) {`
- `public ComponentType getAction() {`
- `public String getDescription() {`
- `public void setDescription( String description ) {`
- `public String getLink() {`
- `public void setLink( String link ) {`
- `public String getContentsStandard() {`
- `public void setContentsStandard( String contents ) {`
- `public String getContentsMobile() {`
- `public void setContentsMobile( String contents ) {`
- `public String getTemplateLanguage() {`
- `public void setTemplateLanguage( String templateLanguage ) {`
- `public boolean isNavbar() {`
- `public void setNavbar( boolean navbar ) {`
- `public boolean isHidden() {`
- `public void setHidden( boolean hidden ) {`
- `public Boolean getAutoContentType() {`
- `public void setAutoContentType(Boolean autoContentType) {`
- `public String getManualContentType() {`
- `public void setManualContentType(String manualContentType) {`
- `public void copyTo(WeblogTemplate dataHolder) throws WebloggerException {`
- `public void copyFrom(WeblogTemplate dataHolder) throws WebloggerException {`
- `public String getMobileTemplateId() {`
- `public void setMobileTemplateId(String mobileTemplateId) {`
- `public String getStandardTemplateId() {`
- `public void setStandardTemplateId(String standardTemplateId) {`
- `public boolean isMobile() {`
- `public String getType() {`
- `public void setType(String type) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/editor/WeblogConfigBean.java
- `public String getHandle() {`
- `public void setHandle( String handle ) {`
- `public String getName() {`
- `public void setName( String name ) {`
- `public String getTagline() {`
- `public void setTagline( String tagline ) {`
- `public boolean getEnableBloggerApi() {`
- `public void setEnableBloggerApi( boolean enableBloggerApi ) {`
- `public String getEditorPage() {`
- `public void setEditorPage( String editorPage ) {`
- `public String getBannedwordslist() {`
- `public void setBannedwordslist( String bannedwordslist ) {`
- `public boolean getAllowComments() {`
- `public void setAllowComments( boolean allowComments ) {`
- `public boolean getDefaultAllowComments() {`
- `public void setDefaultAllowComments( boolean defaultAllowComments ) {`
- `public String getDefaultCommentDays() {`
- `public void setDefaultCommentDays( String defaultCommentDays ) {`
- `public boolean getModerateComments() {`
- `public void setModerateComments( boolean moderateComments ) {`
- `public boolean getEmailComments() {`
- `public void setEmailComments( boolean emailComments ) {`
- `public String getEmailAddress() {`
- `public void setEmailAddress( String emailAddress ) {`
- `public String getLocale() {`
- `public void setLocale( String locale ) {`
- `public String getTimeZone() {`
- `public void setTimeZone( String timeZone ) {`
- `public int getEntryDisplayCount() {`
- `public void setEntryDisplayCount( int entryDisplayCount ) {`
- `public boolean getCommentModerationRequired() {`
- `public void setCommentModerationRequired( boolean commentModerationRequired ) {`
- `public boolean isEnableMultiLang() {`
- `public void setEnableMultiLang( boolean enableMultiLang ) {`
- `public boolean isShowAllLangs() {`
- `public void setShowAllLangs( boolean showAllLangs ) {`
- `public String getIcon() {`
- `public void setIcon(String icon) {`
- `public String getAbout() {`
- `public void setAbout(String about) {`
- `public String getBloggerCategoryId() {`
- `public void setBloggerCategoryId(String bloggerCategoryId) {`
- `public String[] getDefaultPluginsArray() {`
- `public void setDefaultPluginsArray(String[] strings) {`
- `public boolean getApplyCommentDefaults() {`
- `public void setApplyCommentDefaults(boolean applyCommentDefaults) {`
- `public boolean getActive() {`
- `public void setActive(boolean active) {`
- `public String getAnalyticsCode() {`
- `public void setAnalyticsCode(String analyticsCode) {`
- `public void copyFrom(Weblog dataHolder) {`
- `public void copyTo(Weblog dataHolder) {`

## app/src/main/java/org/apache/roller/weblogger/ui/struts2/util/UIAction.java
- `public void myPrepare() {`
- `public void setRequest(Map<String, Object> map) {`
- `public String getSalt() {`
- `public void setSalt(String salt) {`
- `public boolean isUserRequired() {`
- `public boolean isWeblogRequired() {`
- `public List<String> requiredWeblogPermissionActions() {`
- `public List<String> requiredGlobalPermissionActions() {`
- `public boolean isUserIsAdmin() {`
- `public String cancel() {`
- `public String getSiteURL() {`
- `public String getAbsoluteSiteURL() {`
- `public String getProp(String key) {`
- `if(value == null) {`
- `public boolean getBooleanProp(String key) {`
- `if(value == null) {`
- `public int getIntProp(String key) {`
- `if(value == null) {`
- `public String getText(String aTextName) {`
- `public String getText(String aTextName, String defaultValue) {`
- `public String getText(String aTextName, String defaultValue, String obj) {`
- `public String getText(String aTextName, List<?> args) {`
- `public String getText(String key, String[] args) {`
- `public String getText(String aTextName, String defaultValue, List<?> args) {`
- `for (Object el : args) {`
- `public String getText(String key, String defaultValue, String[] args) {`
- `for (int i = 0; i < args.length; ++i) {`
- `public void addError(String errorKey) {`
- `public void addError(String errorKey, String param) {`
- `public void addError(String errorKey, List<?> args) {`
- `public boolean errorsExist() {`
- `public void addMessage(String msgKey) {`
- `public void addMessage(String msgKey, String param) {`
- `public void addMessage(String msgKey, List<?> args) {`
- `public boolean messagesExist() {`
- `public User getAuthenticatedUser() {`
- `public void setAuthenticatedUser(User authenticatedUser) {`
- `public Weblog getActionWeblog() {`
- `public void setActionWeblog(Weblog workingWeblog) {`
- `public String getWeblog() {`
- `public void setWeblog(String weblog) {`
- `public String getPageTitle() {`
- `public void setPageTitle(String pageTitle) {`
- `public String getActionName() {`
- `public void setActionName(String actionName) {`
- `public String getDesiredMenu() {`
- `public void setDesiredMenu(String desiredMenu) {`
- `public Menu getMenu() {`
- `public String getShortDateFormat() {`
- `if (sdf instanceof SimpleDateFormat) {`
- `public String getMediumDateFormat() {`
- `if (sdf instanceof SimpleDateFormat) {`
- `public List<Locale> getLocalesList() {`
- `public List<String> getTimeZonesList() {`
- `public List<Integer> getHoursList() {`
- `public List<Integer> getMinutesList() {`
- `public List<Integer> getSecondsList() {`
- `public List<KeyValueObject> getCommentDaysList() {`
- `private static String cleanExpressions(String s) {`
- `public static String cleanTextKey(String s) {`
- `public static String cleanTextArg(String s) {`
- `private List<?> cleanArgs(List<?> args) {`
- `for (Object arg : args) {`

## app/src/main/java/org/apache/roller/weblogger/util/Utilities.java
- `public static String stripJsessionId(String url) {`
- `if (startPos != -1) {`
- `if (endPos == -1) {`
- `public static String escapeHTML(String s) {`
- `public static String escapeHTML(String s, boolean escapeAmpersand) {`
- `if (escapeAmpersand) {`
- `public static String unescapeHTML(String str) {`
- `public static String removeHTML(String str) {`
- `public static String removeHTML(String str, boolean addSpace) {`
- `if (str == null) {`
- `if (beginTag == -1) {`
- `while (beginTag >= start) {`
- `if (beginTag > 0) {`
- `if (addSpace) {`
- `if (endTag > -1) {`
- `public static String removeAndEscapeHTML(String s) {`
- `if (s == null) {`
- `public static String autoformat(String s) {`
- `public static String addNofollow(String html) {`
- `public static String replaceNonAlphanumeric(String str) {`
- `public static String replaceNonAlphanumeric(String str, char subst) {`
- `for (int i = 0; i < testChars.length; i++) {`
- `public static String removeNonAlphanumeric(String str) {`
- `for (int i = 0; i < testChars.length; i++) {`
- `public static String stringArrayToString(String[] stringArray, String delim) {`
- `for (int i = 0; i < stringArray.length; i++) {`
- `public static String stringListToString(List<String> stringList,
            String delim) {`
- `for (String s : stringList) {`
- `public static String[] stringToStringArray(String instr, String delim) {`
- `public static List<String> stringToStringList(String instr, String delim) {`
- `public static int[] stringToIntArray(String instr, String delim) {`
- `for (String string : str) {`
- `public static String intArrayToString(int[] intArray) {`
- `for (int s : intArray) {`
- `public static void copyFile(File from, File to) throws IOException {`
- `public static String streamToString(InputStream is) throws IOException {`
- `public static void copyInputToOutput(InputStream input,
            OutputStream output, long byteCount) throws IOException {`
- `for (length = byteCount; length > 0;) {`
- `if (bytes < 0) {`
- `public static void copyInputToOutput(InputStream input, OutputStream output)
            throws IOException {`
- `for (int count = 0; count != -1;) {`
- `if (count != -1) {`
- `public static String encodePassword(String password, String algorithm) {`
- `for (int i = 0; i < encodedPassword.length; i++) {`
- `public static String encodeString(String str) throws IOException {`
- `public static String decodeString(String str) throws IOException {`
- `public static String truncate(String str, int lower, int upper,
            String appendToEnd) {`
- `if (upper < lower) {`
- `if (loc >= lower) {`
- `public static String truncateNicely(String str, int lower, int upper,
            String appendToEnd) {`
- `if (upper < lower) {`
- `if (loc >= lower) {`
- `if (diff) {`
- `public static String truncateText(String str, int lower, int upper,
            String appendToEnd) {`
- `if (upper < lower) {`
- `if (loc >= lower) {`
- `private static String stripLineBreaks(String str) {`
- `private static String removeVisibleHTMLTags(String str) {`
- `for (int j = 0; j < visibleTags.length; j++) {`
- `if (endIndex > -1) {`
- `for (int j = 0; j < openCloseTags.length; j++) {`
- `if (endIndex > -1) {`
- `public static String extractHTML(String str) {`
- `if (str == null) {`
- `if (beginTag == -1) {`
- `while (beginTag >= start) {`
- `if (endTag > -1) {`
- `public static String hexEncode(String str) {`
- `public static String encodeEmail(String str) {`
- `public static int stringToInt(String string) {`
- `public static String toBase64(byte[] aValue) {`
- `for (int i = 0; i < iByteLen; i += 3) {`
- `public static String stripInvalidTagCharacters(String tag) {`
- `if (tag == null) {`
- `for (int i = 0; i < charArray.length; i++) {`
- `switch (c) {`
- `public static String normalizeTag(String tag, Locale locale) {`
- `public static List<String> splitStringAsTags(String tags) {`
- `if (tagsarr == null) {`
- `public static String transformToHTMLSubset(String s) {`
- `if (s == null) {`
- `private static String replace(String string, Pattern pattern,
            String replacement) {`
- `public static String getContentTypeFromFileName(String fileName) {`
- `if (map instanceof MimetypesFileTypeMap) {`
- `public static boolean isValidEmailAddress(String aEmailAddress) {`
- `if (aEmailAddress == null) {`
- `private static boolean hasNameAndDomain(String aEmailAddress) {`

## app/src/main/java/org/apache/roller/weblogger/webservices/atomprotocol/RollerAtomHandler.java
- `public RollerAtomHandler(HttpServletRequest request, HttpServletResponse response) {`
- `if (userName != null) {`
- `public String getAuthenticatedUsername() {`
- `if (this.user != null) {`
- `public AtomService getAtomService(AtomRequest areq) throws AtomException {`
- `public Entry postEntry(AtomRequest areq, Entry entry) throws AtomException {`
- `public Entry postMedia(AtomRequest areq, Entry entry)
            throws AtomException {`
- `public Feed getCollection(AtomRequest areq) throws AtomException {`
- `public Categories getCategories(AtomRequest arg0) throws AtomException {`
- `public Entry getEntry(AtomRequest areq) throws AtomException {`
- `if (pathInfo.length > 2) {`
- `public AtomMediaResource getMediaResource(AtomRequest areq) throws AtomException {`
- `public void putEntry(AtomRequest areq, Entry entry) throws AtomException {`
- `public void putMedia(AtomRequest areq) throws AtomException {`
- `public void deleteEntry(AtomRequest areq) throws AtomException {`
- `if (pathInfo.length > 2) {`
- `public boolean isAtomServiceURI(AtomRequest areq) {`
- `public boolean isEntryURI(AtomRequest areq) {`
- `public boolean isMediaEditURI(AtomRequest areq) {`
- `public boolean isCollectionURI(AtomRequest areq) {`
- `public boolean isCategoriesURI(AtomRequest arg0) {`
- `public static boolean canEdit(User u, WeblogEntry entry) {`
- `public static  boolean canEdit(User u, Weblog website) {`
- `public static boolean canView(User u, WeblogEntry entry) {`
- `public static boolean canView(User u, Weblog website) {`
- `protected String authenticateWSSE(HttpServletRequest request) {`
- `if (wsseHeader == null) {`
- `for (int i = 0; i < tokens.length; i++) {`
- `if (index != -1) {`
- `public String authenticateBASIC(HttpServletRequest request) {`
- `if (authHeader != null) {`
- `if (p != -1) {`
- `if (valid) {`
- `private String authenticationOAUTH(
            HttpServletRequest request, HttpServletResponse response) {`
- `public static void oneSecondThrottle() {`
- `if (THROTTLE) {`
- `synchronized (RollerAtomHandler.class) {`
