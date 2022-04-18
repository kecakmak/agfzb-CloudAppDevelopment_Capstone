const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: [{ iamauth: { iamApiKey: params.IAM_API_KEY } },'promises']
    });


   var db = cloudant.db.use('dealerships');


       try {
           let docList = await db.find({selector : { st: params.state }});
           return { docList };
       } catch (error) {
           concolse.log("Something went wrong on the server")
       }


}