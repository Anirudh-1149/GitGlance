import * as React from 'react';
import {  useEffect, useState } from 'react'
import axios from 'axios';
import { CustomCard } from '../components'
import Grid from '@mui/material/Grid';
import { withAuthenticator } from '@aws-amplify/ui-react';

const Explore = ({user}) => {

    const [exploreRepo, setExploreRepo] = useState([])
    const [likedRepos, setLikedRepos] = useState([])

    // useEffect(() => {
    //     axios.get('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/TestStage/api/explore-repositories?userid=45')
    //     .then(function (response) {
    //         console.log('response: ', response);
    //         setExploreRepo(response.data)
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
                    axios.get('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/api/explore-repositories?userid=' + user_id)
                    .then(function (response) {
                        console.log('response: ', response);
                        setExploreRepo(response.data)
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

    return (
        <div>
            <h1 style={{textAlign:'center', marginTop:'5rem'}}>Explore</h1>
            <Grid container spacing={2}>
                {exploreRepo.map(data => (
                    <Grid item xs={6} key={data.repo_url} style={{ height: '100%' }}>
                        <CustomCard content={data} likedRepos={likedRepos} />
                    </Grid>
                ))}
            </Grid>
        </div>
    );
}

export default withAuthenticator(Explore);