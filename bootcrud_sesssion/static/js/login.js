function validate() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // document.write(email)
    // document.write(password);
    // email validation
    if (email == "") {
        document.getElementById('emails').innerHTML = "**PLZ Enter the email";
        // document.getElementById('emails')
        return false;
    }
    if (email.indexOf('@') <= 0) {
        document.getElementById('emails').innerHTML = "**Plz enter valid email";
        // document.getElementById('email').focus();
        return false
    }
    if ((email.charAt(email.length - 4) != '.') && (email.charAt(email.length - 3) != ".")) {
        document.getElementById('emails').innerHTML = "** invalid position of dots..."
            // document.getElementById('email').focus();
        return false
    }

    // password
    if (password == "") {
        document.getElementById('p').innerHTML = "**You cant make it empty"
        return false
    }
    if ((password.length <= 5 || password.length > 20)) {
        document.getElementById('p').innerHTML = "**Password makesure inbetween 6 to 20 character long"
        return false
    }

}