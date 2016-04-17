-- in SQLite3

-- file info, from SRC attribute in IMG tag
create table file_info(
    sha1sum     varchar(50)     -- checksum
,   url         varchar(100)    -- the url source
,   title       varchar(40)     -- the file name
,   time        timestamp       -- the time to get
        NOT NULL DEFAULT (datetime('now','localtime'))
,   primary key (sha1sum, url)
);

-- file description, from ALT attribute in IMG tag.
-- There can be more than one description.
create table file_desc(
    sha1sum         varchar(50)     -- checksum
,   description     varchar(100)    -- the ALT attribute
);
