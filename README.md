# Cloud - GitGlance
GitGlance is designed to simplify the process of finding suitable open-source projects on GitHub for students. This recommendation system filters projects based on language preferences, field of work, and experience level, facilitating more meaningful contributions to the open-source community.


- **Design Prototype**: View the UI/UX design on [Figma](https://www.figma.com/proto/jl6LcC9ho3Qq4WdBqbciZz/CCBD?type=design&node-id=2-597&t=fka5RyfogUtxQxLL-0&scaling=scale-down&page-id=0%3A1&starting-point-node-id=2%3A597).

![demo](/demo/demo.gif)


## Existing Solutions
GitHub currently recommends repositories based on user activities like starring or following, supplemented by manual searches and built-in discovery features. However, these methods are typically time-consuming and may not accurately match user needs. GitGlance leverages advanced recommendation algorithms to offer more precise suggestions, improving upon existing solutions.


## Target Audience
The primary audience for GitGlance is students eager to engage with open-source projects that match their expertise and interests.


## Architecture
![architecture](/demo/architecture.png)


## Instructions to run the application
Follow these instructions to get the application running:
1. Install Node.js version v20.11.0:
   - `nvm install v20.11.0`
   - `nvm use v20.11.0`
2. Install necessary packages:
   - `npm install`
3. Start the application:
   - To run the project : `npm start`


## Technologies used
`aws` `aws-lambda` `s3` `cognito` `api-grateway` `aws-personalize`
