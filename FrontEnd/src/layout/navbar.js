import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Link, useLocation } from 'react-router-dom';
import { signOut } from 'aws-amplify/auth';

export default function ButtonAppBar({children}) {
    const location = useLocation();
    const isCurrentPage = (path) => location.pathname === path;
    const isAuthPage = isCurrentPage('/signin') || isCurrentPage('/signup');

    const handleLogout = async () => {
        // window.location.href = "https://gitglance-domain.auth.us-east-1.amazoncognito.com/logout?client_id=b6uqpn9fne55o855e17rbi8dv&logout_uri=https://gitglance-domain.auth.us-east-1.amazoncognito.com/login?client_id=b6uqpn9fne55o855e17rbi8dv&response_type=code&scope=email+openid+phone&redirect_uri=https%3A%2F%2Fd9lvp3ghzkpxt.cloudfront.net%2F";

        try {
            await signOut(); // Sign out the authenticated user
            // You can also redirect the user to the login page or perform other actions after logout
        } catch (error) {
            console.error('Error signing out:', error);
        }
    };

    return (
        <div>
            {
            !isAuthPage && (
            <AppBar position="static">
                <Toolbar>
                    <div className='navbar_logo'>
                        <svg fill="#ddd" height="45" width="45" aria-hidden="true" viewBox="0 0 16 16" version="1.1" data-view-component="true" className="octicon octicon-mark-github v-align-middle">
                            <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
                        </svg>
                    </div>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        GitGlance
                    </Typography>
                    <Link to="/recommendation" className={isCurrentPage('/recommendation') ? 'nav_active' : 'nav_link'}>Recommendations</Link>
                    <Link to="/" className={isCurrentPage('/') ? 'nav_active' : 'nav_link'}>Preferences</Link>
                    <Link to="/liked" className={isCurrentPage('/liked') ? 'nav_active' : 'nav_link'}>Liked Repositories</Link>
                    <Link to="/explore" className={isCurrentPage('/explore') ? 'nav_active' : 'nav_link'}>Explore</Link>
                    <Link to="/newrepos" className={isCurrentPage('/newrepos') ? 'nav_active' : 'nav_link'}>New Repositories</Link>
                    <Link onClick={handleLogout} className='nav_link'>Logout</Link>
                </Toolbar>
            </AppBar>
        )}
        <div className={!isAuthPage ? 'main_container' : 'App'}>
            <div className='container'>
                {children}
            </div>
        </div>
        </div>
    );
}