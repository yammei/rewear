USE wpdb;

CREATE TABLE products (
  productID INT AUTO_INCREMENT PRIMARY KEY,
  productName VARCHAR(30),
  productDescription VARCHAR(150),
  productPrice DECIMAL(10, 2),
  productType VARCHAR(20),
  productDate DATE,
  productStock TINYINT(1)
);

INSERT INTO products (productName, productDescription, productPrice, productType, productDate, productStock) VALUES
('Widget A', 'High-quality widget with various features.', 19.99, 'Electronics', '2023-05-10', 15),
('Gizmo B', 'Compact gizmo designed for everyday use.', 12.50, 'Gadgets', '2023-06-22', 30),
('Gadget C', 'Cutting-edge gadget for tech enthusiasts.', 49.99, 'Electronics', '2023-04-15', 10),
('Gizmo X', 'Innovative gizmo with advanced functionalities.', 34.75, 'Gadgets', '2023-07-08', 25),
('Widget B', 'Stylish widget with a sleek design.', 22.99, 'Electronics', '2023-05-30', 20);
