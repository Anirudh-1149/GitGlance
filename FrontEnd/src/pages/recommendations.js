import * as React from 'react';
import {  useEffect, useState } from 'react'
import axios from 'axios';
import { CustomCard } from '../components'
import Grid from '@mui/material/Grid';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import { withAuthenticator } from '@aws-amplify/ui-react';

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

const Recommendation = ({user}) => {

    const [recommendedRepo, setRecommendedRepo] = useState([])
    const [languages, setLanguages] = useState([])
    const [likedRepos, setLikedRepos] = useState([])

    // useEffect(() => {
    //     axios.get('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/api/repositories?userid=30')
    //     .then(function (response) {
    //         console.log('response: ', response);
    //         setRecommendedRepo(response.data)
    //     })
    //     .catch(function (error) {
    //         console.log('error: ', error);
    //     })
    // }, [])

    useEffect(() => {
        const data = { user_email: user?.signInDetails?.loginId }
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/getUserData', data)
            .then(function (response) {
                console.log('response: ', response);
                if(response.data.body === "User found") {
                    console.log(response.data.user_data.liked_repos)
                    setLikedRepos(response.data.user_data.liked_repos)
                    const user_id = parseInt(response.data.user_data.user_id) + 50
                    axios.get('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/api/repositories?userid=' + user_id)
                    .then(function (response) {
                        console.log('response: ', response);
                        setRecommendedRepo(response.data)
                    })
                    .catch(function (error) {
                        console.log('error: ', error);
                    })
                }
            })
            .catch(function (error) {
                console.log('error: ', error);
            })
    }, [user])

    const searchFilter = () => {
        const data = {
            language: languages
        }

        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/searchtest/search', data)
        .then(function (response) {
            console.log('response: ', response);
            setRecommendedRepo(response.data.result)
        })
        .catch(function (error) {
            console.log('error: ', error);
        })
    }


    return (
        <div>
            <h1 style={{textAlign:'center', marginTop:'5rem'}}>Recommendations</h1>

            <Autocomplete
                multiple
                options={LANGUAGES}
                getOptionLabel={option => option}
                filterSelectedOptions
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Filter your recommendations by languages"
                        placeholder="languages"
                    />
                )}
                onChange={(e, val) => setLanguages(val)}
            />
            <Button style={{marginTop: '1rem', marginBottom: '3rem'}} fullWidth variant="contained" onClick={searchFilter}>SEARCH</Button>
                
            <Grid container spacing={2}>
                {recommendedRepo && recommendedRepo.map(data => (
                    <Grid item xs={6} key={data.repo_url} style={{ height: '100%' }}>
                        <CustomCard content={data} likedRepos={likedRepos} />
                    </Grid>
                ))}
            </Grid>
        </div>
    );
}

export default withAuthenticator(Recommendation);