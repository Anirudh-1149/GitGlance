import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { withAuthenticator } from '@aws-amplify/ui-react';
import axios from 'axios';

const LANGUAGES = [
    'TypeScript', 
    'PHP',
    'JavaScript',
    'Go',
    'Python',
    'Java',
    'HTML',
    'CSS',
    'Ruby',
    'JSON',
    'YAML'
]

const Preferences = ({ user }) => {
    let navigate = useNavigate();
    const [languages, setLanguages] = useState([])
    const [skipIsDisabled, setSkipIsDisabled] = useState(true)

    const skipHandler = () => {
        navigate("/recommendation");
    }

    useEffect(() => {
        console.log(user)
        const data = {
            "user_email": user?.signInDetails?.loginId
        }
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/getUserData', data)
        .then(function (response) {
            console.log('response: ', response);
            if(response.data.body === "User found") {
                setSkipIsDisabled(false)
                setLanguages(response.data.user_data.preferences)
                console.log(response.data.user_data.preferences)
            }
        })
        .catch(function (error) {
            console.log('error: ', error);
        })
    }, [user])

    const updateHandler = () => {
        const data = {
            user_email: user.signInDetails.loginId,
            user_pref: languages
        }
        console.log(data)
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/userPreferences', data)
        .then(function (response) {
            console.log('response: ', response);
            navigate("/recommendation");
        })
        .catch(function (error) {
            console.log('error: ', error);
        })
    }


    return (
        <div className='auth_container preferences_container'>
            <svg fill="#abb2bb" height="64" width="64" aria-hidden="true" viewBox="0 0 16 16" version="1.1" data-view-component="true" className="octicon octicon-mark-github v-align-middle">
                <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
            </svg>
            <h1>Preferences</h1>
            <br/>

            <div className='container_border_center' style={{padding: '3rem'}}>

                <Autocomplete
                    multiple
                    fullWidth
                    options={LANGUAGES}
                    getOptionLabel={option => option}
                    filterSelectedOptions
                    value={languages}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label="Languages"
                            placeholder="add language to your preferences"
                        />
                    )}
                    onChange={(e,val) => setLanguages(val)}
                />
                
                <div className='button_group'>
                    <Button disabled={skipIsDisabled} fullWidth variant="outlined" color="secondary" onClick={skipHandler}>Skip</Button>
                    <Button fullWidth variant="contained" color="secondary" onClick={updateHandler}>Update</Button>
                </div>

            </div>
        </div>
    );
}

export default withAuthenticator(Preferences);
