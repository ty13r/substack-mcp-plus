export default class SubstackPost {
  constructor({title = null, subtitle = null, user_id, audience = null, write_comment_permissions = null, subscriber_set_id = null }) {
    this.draft_title = title;
    this.draft_subtitle = subtitle;
    this.draft_body = {type: 'doc', content: []};
    this.draft_bylines = [{id: parseInt(user_id), is_guest: false}];
    this.audience = audience !== null ? audience : 'everyone';
    this.draft_section_id = null;
    this.section_chosen = true;

    if (write_comment_permissions !== null) {
      this.write_comment_permissions = write_comment_permissions;
    } else {
      this.write_comment_permissions = this.audience;
    }

    if (subscriber_set_id !== null) {
      this.subscriber_set_id = subscriber_set_id
      this.type = 'adhoc_email'
    }

  }

  setBody(body) {
    this.draft_body = body;
  }

  setTitle(title) {
    this.draft_title = title;
  }

  setSubtitle(subtitle) {
    this.draft_subtitle = subtitle;
  }

  setSection(name, sections) {
    const section = sections.find(s => s.name === name);

    if (!section) {
      throw new Error(`Section ${name} does not exist`);
    }

    this.draft_section_id = section.id;
  }

  add(item) {
    this.draft_body.content = this.draft_body.content || [];
    this.draft_body.content.push({type: item.type});

    const content = item.content;

    if (item.type === 'captionedImage') {
      this.captionedImage(item);
    } else if (item.type === 'youtube2') {
      this.youtube(item.src);
    } else if (item.type === 'subscribeWidget') {
      this.subscribeWithCaption(item.message);
    } else if (item.type === 'bullet_list') {
      this.subscribeWithCaption(item.message);
    } else {
      if (content !== undefined) {
        this.addComplexText(content);
      }
    }

    if (item.type === 'heading') {
      this.attrs(item.level || 1);
    }

    const marks = item.marks;

    if (marks !== undefined) {
      this.marks(marks);
    }

    return this;
  }

  paragraph(content = null) {
    const item = {type: 'paragraph'};

    if (content !== null) {
      item.content = content;
    }

    return this.add(item);
  }

  heading({content = null, level = 1}) {
    const item = {type: 'heading'};

    if (content !== null) {
      item.content = content;
    }

    item.level = level;
    return this.add(item);
  }

  horizontalRule() {
    return this.add({type: 'horizontal_rule'});
  }

  youtubeVideo(resource) {
    const item = {type: 'youtube2'};
    let video_id;
    if (resource.startsWith('http')) {
      const url = new URL(resource);
      // https://www.youtube.com/watch?v=0chZFIZLR_0
      // https://youtu.be/0chZFIZLR_0?si=-Gp9e_RKG3g1SdVG
      video_id = url.searchParams.get('v') || url.pathname.slice(1);
    } else {
      video_id = resource;
    }
    item.src = video_id;
    return this.add(item);
  }

  bulletList(items) {
    this.draft_body.content.push({
      type: 'bullet_list',
      content: items.map(item => {
        const obj = {
          type: 'list_item',
          content: [
            {
              type: 'paragraph',
              content: [{type: 'text', text: item}]
            }
          ]
        }
        return obj
      }),
    });
  }

  orderedList(items) {
    this.draft_body.content.push({
      type: 'ordered_list',
      attrs: {
        start: 1,
        order: 1
      },
      content: items.map(item => {
        const obj = {
          type: 'list_item',
          content: [
            {
              type: 'paragraph',
              content: [{type: 'text', text: item}]
            }
          ]
        }
        return obj
      }),
    });
  }

  italic(text) {
    this.draft_body.content.push({
      type: 'paragraph',
      content: [
        {
          type: 'text',
          marks: [
            {
              type: 'em',
            }
          ],
          text,
        }
      ],
    });
  }

  bold(text) {
    this.draft_body.content.push({
      type: 'paragraph',
      content: [
        {
          type: 'text',
          marks: [
            {
              type: 'strong',
            }
          ],
          text,
        }
      ],
    });
  }

  paywall() {
    this.draft_body.content.push({
      type: 'paywall'
    });
  }

  shareButton() {
    this.draft_body.content.push({
      type: 'button',
      attrs: {
        url: '%%share_url%%',
        text: 'Share',
        action: null,
        class: 'button-wrapper'
      }
    });
  }

  commentButton() {
    this.draft_body.content.push({
      type: 'button',
      attrs: {
        url: '%%half_magic_comments_url%%',
        text: 'Leave a comment',
        action: null,
        class: 'button-wrapper'
      }
    });
  }

  customButton({url, text}) {
    this.draft_body.content.push({
      type: 'button',
      attrs: {
        url,
        text,
        action: null,
        class: 'button-wrapper'
      }
    });
  }

  customSubscribeButton() {
    this.customButton({url: "https://quickviewai.substack.com/subscribe?", text: 'Get full access to Quickview ✨'});
  }

  addHeader({summaries_length}) {
    const header = [
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":"Hey, "
          },
          {
            "type":"text",
            "marks":[
              {
                "type":"strong"
              }
            ],
            "text":"Marco"
          },
          {
            "type":"text",
            "text":" here! Welcome to the "
          },
          {
            "type":"text",
            "marks":[
              {
                "type":"strong"
              }
            ],
            "text":"Crypto Daily Recap"
          },
          {
            "type":"text",
            "text":" 💡"
          }
        ]
      },
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":`Every day, I send you an email with a curated collection of highlights from the Crypto universe. In this newsletter, you'll discover ${summaries_length} insightful summaries covering intriguing topics:`
          }
        ]
      }
    ]
    this.draft_body.content.push(...header)
  }

  addHeaderTopics(topics) {
    const topics_list =     {
      "type":"bullet_list",
      "content": topics.map((topic) => {
        return {
          "type": "list_item",
          "content": [
            {
              "type": "paragraph",
              "content":[
                {
                  "type": "text",
                  "text": topic
                }
              ]
            }
          ]
        }
      })
    }

    this.draft_body.content.push(topics_list)
  }

  becamePremiumMember() {
    const section = [
      {
        "type":"horizontal_rule"
      },
      {
        "type":"heading",
        "attrs":{
          "level":2
        },
        "content":[
          {
            "type":"text",
            "text":"🌟 Become a premium member, don't miss out!"
          }
        ]
      },
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":"Free users access summaries for only 2 videos daily, elevate your experience with premium for:"
          }
        ]
      },
      {
        "type":"bullet_list",
        "content":[
          {
            "type":"list_item",
            "content":[
              {
                "type":"paragraph",
                "content":[
                  {
                    "type":"text",
                    "text":"📄 "
                  },
                  {
                    "type":"text",
                    "marks":[
                      {
                        "type":"strong"
                      }
                    ],
                    "text":"Complete summaries"
                  },
                  {
                    "type":"text",
                    "text":": Dive deep into every video."
                  }
                ]
              }
            ]
          },
          {
            "type":"list_item",
            "content":[
              {
                "type":"paragraph",
                "content":[
                  {
                    "type":"text",
                    "text":"🚀 "
                  },
                  {
                    "type":"text",
                    "marks":[
                      {
                        "type":"strong"
                      }
                    ],
                    "text":"Early access"
                  },
                  {
                    "type":"text",
                    "text":": Get the insights before anyone else."
                  }
                ]
              }
            ]
          },
          {
            "type":"list_item",
            "content":[
              {
                "type":"paragraph",
                "content":[
                  {
                    "type":"text",
                    "text":"🎤 "
                  },
                  {
                    "type":"text",
                    "marks":[
                      {
                        "type":"strong"
                      }
                    ],
                    "text":"Exclusive voiceovers"
                  },
                  {
                    "type":"text",
                    "text":": Enhance your experience with exclusive voiceovers for a better experience."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "type": "blockquote",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Share the article with someone who would like it, and "
              },
              {
                "type": "text",
                "marks": [
                  {
                    "type": "strong"
                  }
                ],
                "text": "get a free membership"
              },
              {
                "type": "text",
                "text": " through the new "
              },
              {
                "type": "text",
                "marks": [
                  {
                    "type": "link",
                    "attrs": {
                      "href": "https://quickviewai.substack.com/p/invite-your-friends-and-get-quickview",
                      "target": "_blank",
                      "rel": "",
                      "class": null
                    }
                  }
                ],
                "text": "referral program"
              },
              {
                "type": "text",
                "text": "."
              }
            ]
          }
        ]
      },
      {
        "type":"button",
        "attrs":{
          "url":"https://quickviewai.substack.com/subscribe?",
          "text":"Get full access to Quickview ✨",
          "action":null,
          "class":"button-wrapper"
        }
      },
      {
        "type":"horizontal_rule"
      }
    ]

    this.draft_body.content.push(...section)
  }

  addFooter() {
    const footer = [
      {
        "type":"horizontal_rule"
      },
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":"And that’s it for today! If you are finding this newsletter valuable, consider doing any of these:"
          }
        ]
      },
      {
        "type":"ordered_list",
        "attrs":{
          "start":1,
          "order":1
        },
        "content":[
          {
            "type":"list_item",
            "content":[
              {
                "type":"paragraph",
                "content":[
                  {
                    "type":"text",
                    "text":"🍻 "
                  },
                  {
                    "type":"text",
                    "marks":[
                      {
                        "type":"strong"
                      }
                    ],
                    "text":"Read with your friends"
                  },
                  {
                    "type":"text",
                    "text":" — Quickview lives thanks to word of mouth. Share the article with someone who would like it."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "type":"button",
        "attrs":{
          "url":"%%share_url%%",
          "text":"Share",
          "action":null,
          "class":"button-wrapper"
        }
      },
      {
        "type":"ordered_list",
        "attrs":{
          "start":2,
          "order":2
        },
        "content":[
          {
            "type":"list_item",
            "content":[
              {
                "type":"paragraph",
                "content":[
                  {
                    "type":"text",
                    "text":"📣 "
                  },
                  {
                    "type":"text",
                    "marks":[
                      {
                        "type":"strong"
                      }
                    ],
                    "text":"Provide your feedback"
                  },
                  {
                    "type":"text",
                    "text":" - We welcome your thoughts! Please share your opinions or suggestions for improving the newsletter, your input helps us adapt the content to your tastes."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "type":"button",
        "attrs":{
          "url":"%%half_magic_comments_url%%",
          "text":"Leave a comment",
          "action":null,
          "class":"button-wrapper"
        }
      },
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":"I wish you a great day! ☀️"
          }
        ]
      },
      {
        "type":"paragraph",
        "content":[
          {
            "type":"text",
            "text":"Marco"
          }
        ]
      }
    ]
    this.draft_body.content.push(...footer)
  }

  attrs(level) {
    const contentAttrs = this.draft_body.content[this.draft_body.content.length - 1].attrs || {};
    contentAttrs.level = level;
    this.draft_body.content[this.draft_body.content.length - 1].attrs = contentAttrs;
    return this;
  }

  captionedImage({
                   src,
                   fullscreen = false,
                   imageSize = 'normal',
                   height = 819,
                   width = 1456,
                   resizeWidth = 728,
                   bytes = null,
                   alt = null,
                   title = null,
                   type = null,
                   href = null,
                   belowTheFold = false,
                   internalRedirect = null,
                 }) {
    const content = this.draft_body.content[this.draft_body.content.length - 1].content || [];
    content.push({
      type: 'image2',
      attrs: {
        src,
        fullscreen,
        imageSize,
        height,
        width,
        resizeWidth,
        bytes,
        alt,
        title,
        type,
        href,
        belowTheFold,
        internalRedirect,
      },
    });

    this.draft_body.content[this.draft_body.content.length - 1].content = content;
    return this;
  }

  text(value) {
    const content = this.draft_body.content[this.draft_body.content.length - 1].content || [];
    content.push({type: 'text', text: value});
    this.draft_body.content[this.draft_body.content.length - 1].content = content;
    return this;
  }

  addComplexText(text) {
    if (typeof text === 'string') {
      this.text(text);
    } else {
      text.forEach(chunk => {
        if (chunk) {
          this.text(chunk.content).marks(chunk.marks || []);
        }
      });
    }
  }

  marks(marks) {
    const content = this.draft_body.content[this.draft_body.content.length - 1].content.slice(-1)[0];
    const contentMarks = content.marks || [];

    marks.forEach(mark => {
      const newMark = {type: mark.type};

      if (mark.type === 'link') {
        const href = mark.href;
        newMark.attrs = {href};
      }

      contentMarks.push(newMark);
    });

    content.marks = contentMarks;
    return this;
  }

  removeLastParagraph() {
    this.draft_body.content.pop();
  }

  getDraft() {
    const {draft_body, ...rest} = this;
    return {...rest, draft_body: JSON.stringify(draft_body)};
  }

  subscribeWithCaption(message = null) {
    if (message === null) {
      message = `Thanks for reading this newsletter!
      Subscribe for free to receive new posts and support my work.`;
    }

    const subscribe = this.draft_body.content[this.draft_body.content.length - 1];
    subscribe.attrs = {url: '%%checkout_url%%', text: 'Subscribe', language: 'en'};
    subscribe.content = [
      {
        type: 'ctaCaption',
        content: [
          {
            type: 'text',
            text: message,
          },
        ],
      },
    ];

    return this;
  }

  youtube(value) {
    const contentAttrs = this.draft_body.content[this.draft_body.content.length - 1].attrs || {};
    contentAttrs.videoId = value;
    this.draft_body.content[this.draft_body.content.length - 1].attrs = contentAttrs;
    return this;
  }
}
