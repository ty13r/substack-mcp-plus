import {z} from "zod";


export const createDraftPostSchema = z.object({
  text: z
    .string()
    .describe(
      "The text of the post to be created."
    ),
});

export const createDraftPostHandler = async (args) => {
  const validatedArgs = createDraftPostSchema.parse(args);

  const { text } = validatedArgs;

  return text
}