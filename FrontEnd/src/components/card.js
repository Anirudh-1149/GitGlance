import * as React from 'react';
import axios from 'axios'
import { withAuthenticator } from '@aws-amplify/ui-react';
import { useNavigate } from 'react-router-dom';


const CustomCard = ({content, user, likedRepos}) => {
    const navigate = useNavigate();
    

    const linkClickHandler = () => {
        const data = {
            "EVENT_TYPE" : "click",
            "ITEM_ID" : content.repo_url,
            "TIMESTAMP" : Math.floor(Date.now() / 1000),
            "USER_ID" : "30"
        }

        const postData = {
            StreamName: "repos-interaction-stream",
            Data: btoa(JSON.stringify(data)),
            PartitionKey: "30"
        }

        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/TestStage/api/interactions', postData)
        .then(function (response) {
            console.log('response click: ', response);
        })
        .catch(function (error) {
            console.log('error click: ', error);
        });
    }

    const likeClickHandler = () => {

        const ml_data = {
            "EVENT_TYPE" : "like",
            "ITEM_ID" : content.repo_url,
            "TIMESTAMP" : Math.floor(Date.now() / 1000),
            "USER_ID" : "30"
        }
        const ml_postData = {
            StreamName: "repos-interaction-stream",
            Data: btoa(JSON.stringify(ml_data)),
            PartitionKey: "30"
        }
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/TestStage/api/interactions', ml_postData)
        .then(function (response) {
            console.log('response like: ', response);
        })
        .catch(function (error) {
            console.log('error like: ', error);
        });

        const like_data = {
            user_email: user?.signInDetails?.loginId,
            repo_url: [content.repo_url],
            action: likedRepos?.includes(content.repo_url) ? "unlike" : "like"
        }
        axios.post('https://rwrbehkr47.execute-api.us-east-1.amazonaws.com/update_pref/recordLike', like_data)
        .then(function (response) {
            console.log('response like: ', response);
            navigate(0);
        })
        .catch(function (error) {
            console.log('error like: ', error);
        });
    }

    return (
        <div className='card_container'>
            <div onClick={linkClickHandler}>
                <a className='topic_link' href={content.repo_url} rel="noreferrer" target="_blank">
                    <p>{content.title}</p>
                </a>
            </div>
            <p>{content.language[0]} {content.language[1] ? '/ ' + content.language[1] : null}</p>
            <br/>
            <p className='card_like' style={{color: likedRepos.includes(content.repo_url) ? '#9A2D1E' : '#B4B4B4'}} onClick={likeClickHandler}>Like</p>
        </div>
    );
}

export default withAuthenticator(CustomCard);