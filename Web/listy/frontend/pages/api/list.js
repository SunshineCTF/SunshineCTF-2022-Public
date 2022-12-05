const LEADERBOARD_FUNCTION = 'listy';
const LEADERBOARD_PROJECT = 'sunshine-2022-challenges'
const BUCKET_NAME = 'ssctf22-listy-leaderboard-prod'
const LOCAL_DEV = true ? process.env.LOCAL_DEV : false
const GCLOUD_TOKEN = process.env.GCLOUD_TOKEN

const {
    GoogleAuth
} = require('google-auth-library');
const auth = new GoogleAuth();

export default async (req, res) => {
    if (LOCAL_DEV) {
        res.status(200).json([{
            "rank": 1,
            "username": "Bill",
            "points": 100
        }, {
            "rank": 2,
            "username": "SpongeBob",
            "points": 50
        }])
        return
    }

    const url = `https://us-central1-${LEADERBOARD_PROJECT}.cloudfunctions.net/${LEADERBOARD_FUNCTION}?bucket=${BUCKET_NAME}`
    const audience = url.split("\?")[0]
    console.log("Audience: " + audience)
    const client = await auth.getIdTokenClient(audience);

    let response = await client.request({
        url
    })

    try {
        console.log('response', response)
        const data = await response.data;
        res.status(200).json(data);
    } catch (e) {
        if (e.message.includes("accounts.google.com")) {
            res.status(401).json({
                error: "Backend Authentication Error."
            })
        } else {
            res.status(500).json({
                error: e
            });
        }
    }
}