

function insertProductData()  {

    // Create data object
    const data = {
    productID,
    productName: 'White T-Shirt',
    productDescription: 'A plain white tee.',
    productPrice: parseFloat(8.99),
    productType: 'Shirt',
    productDate: '05-05-2023',
    productStock: parseInt(1)
    };

    // Send HTTP POST request to server
    try {
    const response = await fetch('http://localhost:8080/insert', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // Handle response
    if (response.ok) {
        // Success
        alert('Form submitted successfully');
    } else {
        // Error
        alert('Error submitting form');
    }
    } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while submitting the form');
    }
}

