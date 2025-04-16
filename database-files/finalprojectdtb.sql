CREATE DATABASE final;
USE final;
CREATE TABLE Users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    trust_score FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Items (
    item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    estimated_value DECIMAL(10,2),
    status VARCHAR(50) CHECK (status IN ('Available', 'Traded', 'Pending')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Trades (
    trade_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    proposer_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    status VARCHAR(50) CHECK (status IN ('Proposed', 'Accepted', 'Declined', 'Completed')),
    fairness_score FLOAT,
    cash_adjustment DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proposer_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Trade_Items (
    trade_item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    trade_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    offered_by BIGINT NOT NULL,
    FOREIGN KEY (trade_id) REFERENCES Trades(trade_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE,
    FOREIGN KEY (offered_by) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    trade_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (trade_id) REFERENCES Trades(trade_id) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    review_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reviewer_id BIGINT NOT NULL,
    reviewed_id BIGINT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewer_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Payments (
    payment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    trade_id BIGINT NOT NULL,
    payer_id BIGINT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('Pending', 'Completed', 'Failed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trade_id) REFERENCES Trades(trade_id) ON DELETE CASCADE,
    FOREIGN KEY (payer_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Fraud_Reports (
    report_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    trade_id BIGINT NOT NULL,
    reported_by BIGINT NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) CHECK (status IN ('Under Review', 'Resolved', 'Dismissed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trade_id) REFERENCES Trades(trade_id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    action TEXT NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL
);

CREATE TABLE Analytics (
    analytics_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    metric VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Users (username, email, password_hash, trust_score) VALUES
('jake_sneakerhead', 'jake@example.com', 'hashed_password1', 80),
('emma_reseller', 'emma@example.com', 'hashed_password2', 90),
('lisa_admin', 'lisa@example.com', 'hashed_password3', 95),
('raj_analyst', 'raj@example.com', 'hashed_password4', 85);

INSERT INTO Items (user_id, title, description, category, estimated_value, status) VALUES
(1, 'Air Jordan 1', 'Rare edition, barely worn', 'Sneakers', 250.00, 'Available'),
(1, 'Yeezy Boost 350', 'Used but in great condition', 'Sneakers', 200.00, 'Available'),
(2, 'iPhone 12', '128GB, factory unlocked', 'Electronics', 500.00, 'Available'),
(2, 'PS5 Console', 'Brand new, unopened', 'Gaming', 600.00, 'Available');

INSERT INTO Trades (proposer_id, receiver_id, status, fairness_score, cash_adjustment) VALUES
(1, 2, 'Proposed', 85.5, 50.00),  -- Trade from Jake to Emma
(2, 1, 'Proposed', 90.0, 0.00),  -- Trade from Emma to Jake
(3, 4, 'Proposed', 92.0, 30.00),  -- Trade from Lisa to Raj
(4, 3, 'Proposed', 88.0, 40.00);  -- Trade from Raj to Lisa

INSERT INTO Trades (proposer_id, receiver_id, status, fairness_score, cash_adjustment) VALUES
(1, 2, 'Proposed', 85.5, 50.00),
(2, 1, 'Accepted', 90.0, 0.00);

INSERT INTO Trade_Items (trade_id, item_id, offered_by) VALUES
(1, 1, 1),
(1, 3, 2),
(2, 2, 1),
(2, 4, 2);

INSERT INTO Messages (sender_id, receiver_id, trade_id, content) VALUES
(1, 2, 1, 'Hey, would you consider adding some cash to balance this trade?'),
(2, 1, 1, 'Sure, how about $50?'),
(2, 1, 2, 'Thanks for accepting the trade!');

INSERT INTO Reviews (reviewer_id, reviewed_id, rating, comment) VALUES
(1, 2, 5, 'Great trader, highly recommended!'),
(2, 1, 4, 'Smooth transaction, would trade again.');

INSERT INTO Payments (trade_id, payer_id, amount, status) VALUES
(1, 1, 50.00, 'Completed');

INSERT INTO Fraud_Reports (trade_id, reported_by, reason, status) VALUES
(1, 2, 'Suspected counterfeit sneakers', 'Under Review');

INSERT INTO Logs (user_id, action) VALUES
(1, 'Trade proposed'),
(2, 'Trade accepted'),
(1, 'Review submitted');

INSERT INTO Analytics (metric, value) VALUES
('Total Trades', 2),
('Average Fairness Score', 87.75);
