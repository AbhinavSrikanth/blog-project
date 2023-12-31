document.addEventListener('DOMContentLoaded', () => {
    const accountCreation = document.querySelector('.accountcreation');
  
    accountCreation.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm_password').value;
  
      if (password !== confirmPassword) {
        alert('Passwords do not match. Please try again');
        return;
      }
      try {
        const response = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            confirm_password: confirmPassword
          })
        });
  
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          window.location.href='http://127.0.0.1:5000/login_land';
        } else {
          const errorData = await response.json();
          window.location.href='http://127.0.0.1:5000/accountcreation'
          alert("error: " + errorData.error);
        }
      } catch (error) {
        console.log('Error:', error);
        alert('An error occurred. Please try again later.');
      }
    });
    const loginButton=document.getElementById('loginButton');
    loginButton.addEventListener('click', () => {
      window.location.href = 'http://127.0.0.1:5000/login_land';
    });
  });
  