import {useEffect} from "react";

export function useAuth(login, password) {
    // send request to localhost:8000/api/v1/login OAuth2 endpoint
    // if success, redirect to /profile
    // if fail, show error message

    var details = {
    'username': login,
    'password': password,
    'grant_type': 'password'
    };

    var formBody = [];
    for (var property in details) {
      var encodedKey = encodeURIComponent(property);
      var encodedValue = encodeURIComponent(details[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    console.log(formBody);

    fetch('http://localhost:8000/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        // body is string
        body: formBody
    })
    .then(response => {
        if (response.status === 401) {
            console.log('Incorrect credentials');
            return null;
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data == null) return;

        console.log('Success:', data);

        // set token to localStorage
        localStorage.setItem('access_token', data.access_token);

        // redirect to /
        window.location.href = '/';

    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }

  export function checkAuth() {
    return useEffect(() => {
      const access_token = localStorage.getItem('access_token');

      // if access_token in local storage, logical if
      if (access_token != null) {
        // request to /api/v1/users/me, if status code 200, redirect to /
        fetch('http://192.168.1.68:8000/api/v1/users/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        })
        .then(response => {
            return response.status === 200;

        })
        .catch((error) => {
            console.error('Error:', error);
            return false;
        });
      }
    }, []);
  }