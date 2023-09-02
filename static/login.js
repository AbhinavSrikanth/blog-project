document.addEventListener('DOMContentLoaded', ()=>{
    const loginform=document.querySelector('.login');
    loginform.addEventListener('submit',async(event)=>{
        event.preventDefault();
        const email=document.getElementById('email').value;
        const password=document.getElementById('password').value;
        console.log('Email:',email)
        console.log('Password:',password)

        if(!email||!password){
            alert('Please provide both email and password')
            return;
        } else{
        try{
            const response=await fetch('http://127.0.0.1:5000/login_auth',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({
                    email: email,
                    password: password
                })
            });

           if (response.ok) {
          const data = await response.json();
          alert(data.message);
          window.location.href='http://127.0.0.1:5000/home';
        } else {
          const errorData = await response.json();
          alert("error: " + errorData.error);
        }
        } catch(error){
            console.log('Error Details',error)
            alert('An error occurred. Please try again later.');
        }
    }
    });
});