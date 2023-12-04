// const{Configuration, OpenAIApi} = require('openai-api');
// const configuration = new Configuration({apiKey: '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'})
// const openai = new OpenAIApi(configuration);

const OpenAI = require('openai');
const openai = new OpenAI({
  apiKey: '', dangerouslyAllowBrowser: true
});

export async function sendMsgToOpenAI(message) {
    const res = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        prompt: 'message',
        max_tokens: 30,

    })

    return res.choices[0].message.content;
}

// const chatCompletion = await openai.chat.completions.create({
//     model: "gpt-3.5-turbo",
//     prompt: 'message',
//     max_tokens: 30,
//   });
//   console.log(chatCompletion.choices[0].message);

//   model : 'text-2',
//   prompt : message,
//   temperature : 0.9, 
//   maxTokens : 256,
//   top_p : 1,  
//   frequency_penalty : 0.0,
//   presense_penalty : 0.0,     