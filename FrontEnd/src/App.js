import { SignUp, SignIn, Recommendation, Liked, Explore, Preferences, Newrepos } from './pages'
import ButtonAppBar from './layout/navbar'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';


const awsExports = {
  "aws_project_region": "us-east-1",
  "aws_cognito_identity_pool_id": "us-east-1:e49f96e0-a66b-490a-a10e-e73011994172",
  "aws_cognito_region": "us-east-1",
  "aws_user_pools_id": "us-east-1_k8gUVvg59",
  "aws_user_pools_web_client_id": "7399h1re77indd7u5eoaa4bu31",
  "oauth": {},
  "aws_cognito_username_attributes": [
      "EMAIL"
  ],
  "aws_cognito_social_providers": [],
  "aws_cognito_signup_attributes": [
      "EMAIL"
  ],
  "aws_cognito_mfa_configuration": "OFF",
  "aws_cognito_mfa_types": [
      "SMS"
  ],
  "aws_cognito_password_protection_settings": {
      "passwordPolicyMinLength": 8,
      "passwordPolicyCharacters": []
  },
  "aws_cognito_verification_mechanisms": [
      "EMAIL"
  ]
};


Amplify.configure(awsExports);


function App() {
  return (
    <Router>
        <ButtonAppBar>
        <Routes>
          <Route path="/signup" element={<SignUp />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/explore" element={<Explore/>}/>
          <Route path="/recommendation" element={<Recommendation />} />
          <Route path="/liked" element={<Liked />} />
          <Route path="/newrepos" element={<Newrepos/>}/>
          <Route path="/" element={<Preferences />} />
        </Routes>
        </ButtonAppBar>
    </Router>
  );
}

export default withAuthenticator(App, { includeGreetings: true, loginMechanisms: ['email'] });