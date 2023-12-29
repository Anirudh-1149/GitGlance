import React, { useEffect, useState } from 'react';
import { CustomLikeCard } from '../components'
import Grid from '@mui/material/Grid';
import { withAuthenticator } from '@aws-amplify/ui-react';
import axios from 'axios'

const Liked = ({user}) => {

    const [likedRepos, setLikedRepo] = useState()
    const [isUserLikedRepo, setIsUserLikedRepo] = useState(false)

    useEffect(() => {
        const data = {
            "user_email": user?.signInDetails?.loginId
        }
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/getUserData', data)
            .then(function (response) {
                console.log('response: ', response);
                if(response.data.body === "No User Found") {
                    setIsUserLikedRepo(false)
                } else if(response.data.body === "User found") {
                    setIsUserLikedRepo(true)
                    console.log(response.data.user_data.liked_repos)
                    setLikedRepo(response.data.user_data.liked_repos)
                }
            })
            .catch(function (error) {
                console.log('error: ', error);
            })

    }, [user])

    return (
        <div>
            {isUserLikedRepo ? (
                <>
                    <h1 style={{textAlign:'center', marginTop:'5rem'}}>User's Liked Repositories</h1>
                    <Grid container spacing={2}>
                        {likedRepos.map(likedRepo => (
                            <Grid item xs={12} key={likedRepo}>
                                <CustomLikeCard link={likedRepo} />
                            </Grid>
                        ))}
                    </Grid>
                </>
            ) : <h1>User has not updated their preferences!</h1> }
        </div>
    );
}

export default withAuthenticator(Liked);