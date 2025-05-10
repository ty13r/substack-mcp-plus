import {z} from "zod";
import SubstackApi from "../api/substack/SubstackApi.js";
import SubstackPost from "../api/substack/SubstackPost.js";


export const createDraftPostSchema = z.object({
  title: z
    .string()
    .describe(
      "The title of the post to be created."
    ),
  subtitle: z
    .string()
    .describe(
      "The subtitle of the post to be created."
    ),
  body: z
    .string()
    .describe(
      "The body of the post to be created."
    ),
});

export const createDraftPostHandler = async (args) => {
  const validatedArgs = createDraftPostSchema.parse(args);

  const {title, subtitle, body} = validatedArgs;

  const substack_api = new SubstackApi({
    publication_url: process.env.SUBSTACK_PUBLICATION_URL,
    auth_token: process.env.SUBSTACK_SESSION_TOKEN,
  })

  const substack_post = new SubstackPost({user_id: process.env.SUBSTACK_USER_ID});

  substack_post.setTitle(title)
  substack_post.setSubtitle(subtitle)
  substack_post.setBody(body)

  await substack_api.postDraft(substack_post.getDraft())

  return 'OK'
}