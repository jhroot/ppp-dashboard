
-- tables
-- Table: Item
CREATE TABLE Item (
    item_id int  NOT NULL,
    item_identifier varchar(512)  NOT NULL,
    version int  NOT NULL,
    run int  NOT NULL,
    CONSTRAINT Item_pk PRIMARY KEY (item_id)
);

CREATE INDEX Item_idx_1 on Item (item_id ASC);




-- Table: event
CREATE TABLE event (
    event_id int  NOT NULL,
    version int  NOT NULL,
    run int  NOT NULL,
    type varchar(255)  NOT NULL,
    timestamp timestamp  NOT NULL,
    status varchar(255)  NOT NULL,
    message text  NULL,
    item_id int  NOT NULL,
    CONSTRAINT event_pk PRIMARY KEY (event_id)
);

CREATE INDEX event_idx_1 on event (version ASC,run ASC,item_id ASC);




-- Table: property
CREATE TABLE property (
    property_id int  NOT NULL,
    name varchar(255)  NOT NULL,
    int_value int  NULL,
    text_value text  NULL,
    date_value int  NULL,
    property_type varchar(255)  NOT NULL,
    item_id int  NOT NULL,
    CONSTRAINT property_pk PRIMARY KEY (property_id)
);

CREATE INDEX property_idx_1 on property (item_id ASC);








-- foreign keys
-- Reference:  event_Item (table: event)


ALTER TABLE event ADD CONSTRAINT event_Item 
    FOREIGN KEY (item_id)
    REFERENCES Item (item_id)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  property_Item (table: property)


ALTER TABLE property ADD CONSTRAINT property_Item 
    FOREIGN KEY (item_id)
    REFERENCES Item (item_id)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

