import { client } from '../client/client.gen';

client.setConfig({
    baseUrl: '/api/v1',
    credentials: 'include',
});

client.interceptors.response.use(async (response) => {
    if (response.status === 401) {
        console.warn("401 Unauthorized, redirecting...");
        window.location.href = "/login";
    }
    return response;
});
