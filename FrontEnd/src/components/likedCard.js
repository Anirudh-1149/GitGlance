import React from 'react';

const CustomLikeCard = ({link}) => {
    return (
        <div className='card_container'>
            <a className='topic_link' href={link} rel="noreferrer" target="_blank">
                <p>{link}</p>
            </a>
        </div>
    );
}

export default CustomLikeCard;