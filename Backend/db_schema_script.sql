PRAGMA foreign_keys = ON;

CREATE TABLE user_info (
    id TEXT UNIQUE DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT NOT NULL
);

CREATE TABLE user_jwt (
    user_id TEXT PRIMARY KEY NOT NULL,
    jwt TEXT NOT NULL,
    last_logged_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE service_info (
    service_id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    description TEXT NOT NULL,
    currency TEXT NOT NULL,
    base_price DECIMAL(10,2) not null,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE service_professional_info (
    service_professional_id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    service_keywords TEXT NULL,
    service_id TEXT NULL,
    experience_years INTEGER NOT NULL,
    location TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    pincode TEXT NOT NULL,
    record_status TEXT NOT NULL DEFAULT 'U',
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE service_professional_documents (
    document_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    service_professional_id TEXT NOT NULL,
    document_name TEXT NOT NULL,
    document_type TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified TEXT DEFAULT 'NOT VERIFIED',
    document_data BLOB NOT NULL,
    PRIMARY KEY (document_id),
    FOREIGN KEY (service_professional_id) REFERENCES service_professional_info(service_professional_id)
);


CREATE TABLE customer_info (
    customer_id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT UNIQUE NOT NULL,
    location TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    pincode TEXT NOT NULL,
    BLOCKED TEXT NOT NULL DEFAULT 'NOT BLOCKED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

CREATE TABLE booking_info (
    booking_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    service_professional_id INTEGER NOT NULL,
    customer_id TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status TEXT NOT NULL,
    currency TEXT NOT NULL,
    price DECIMAL(10,2) not null,
    service_professional_remarks TEXT,
    customer_rating INTEGER,
    PRIMARY KEY (booking_id),
    FOREIGN KEY (service_professional_id) REFERENCES service_professional_info(user_id),
    FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
);

CREATE TABLE request_info (
    request_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    customer_id INTEGER NOT NULL,
    keywords TEXT NOT NULL,
    service_id TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    currency TEXT NOT NULL,
    quote_price DECIMAL(10,2) not null,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (request_id),
    FOREIGN KEY (customer_id) REFERENCES customer_info(user_id),
    FOREIGN KEY (service_id) REFERENCES service_info(service_id)
);

CREATE TABLE reviews_info (
    review_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    service_professional_id TEXT NOT NULL,
    booking_id TEXT NOT NULL,
    service_professional_rating INTEGER,
    review_provided TEXT NOT NULL,
    customer_remarks TEXT,
    currency TEXT NOT NULL,
    paid_price DECIMAL(10,2) not null,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_given_time TIMESTAMP,
    PRIMARY KEY (review_id),
    FOREIGN KEY (service_professional_id) REFERENCES service_professional_info(service_professional_id),
    FOREIGN KEY (booking_id) REFERENCES booking_info(booking_id)
);
