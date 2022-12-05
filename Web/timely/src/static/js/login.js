function validate(a) {
    unameObj = document.getElementById('username')
    passObj = document.getElementById('password')

    hashObj = new jsSHA("SHA-1", "TEXT", {
        numRounds: 1
    });
    hashObj.update(passObj.value)
    hash = hashObj.getHash("HEX");
    console.log(hash)

    xhr = new XMLHttpRequest()
    xhr.open("POST", "/login")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(JSON.stringify({
        "username": unameObj.value,
        "password": hash
    }))


    xhr.onload = (e) => {
        // console.log("Received Response!")
        console.log(e)
        if (e.currentTarget.status == 401) {
            document.getElementById('error').innerHTML = `Error: ${e.currentTarget.response}`
        } else {
            document.getElementById('flag').innerHTML = `WOW!: ${e.currentTarget.response}`
        }
    }
}