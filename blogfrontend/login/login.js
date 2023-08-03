document.addEventListener('DOMContentLoaded',()=>{
    const loginForm=document.querySelector('.login');
    if(loginForm){
    loginForm.addEventListener('submit',async(event)=>{
        event.preventDefault();
        const email=document.getElementById('email').value;
        const password=document.getElementById('password').value;
        console.log('Email:',email)
        console.log('Password:',password)

        if(!email||!password){
            alert('Please provide both email and password')
            return
        }
        try{
            const response=await fetch('http://127.0.0.1:5000/login',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({
                    email:email,
                    password:password
                })
            });
            if(response.ok){
                window.location.href='/blogfrontend/home/home.html';
            } else{
                const errorData=await response.json();
                alert(errorData.error);
            }
        } catch(error){
            console.error('Error',error);
            alert('An error occurred. Please try again later.');
        }
    });
    }
});