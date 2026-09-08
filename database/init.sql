CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    vip BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total NUMERIC(10, 2) NOT NULL CHECK (total >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE support_tickets (
    ticket_id BIGSERIAL PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_id TEXT,
    category TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

INSERT INTO customers (customer_id, name, email, vip)
VALUES
    ('CUST-001', 'Anna', 'anna@example.com', true),
    ('CUST-002', 'Bob', 'bob@example.com', false),
    ('CUST-003', 'Chris', 'chris@example.com', false);

INSERT INTO orders (order_id, customer_id, status, total)
VALUES
    ('ORD-001', 'CUST-001', 'paid', 199.99),
    ('ORD-002', 'CUST-001', 'shipped', 349.50),
    ('ORD-003', 'CUST-002', 'processing', 89.00),
    ('ORD-004', 'CUST-003', 'delivered', 520.00);
