import axios from 'axios';

export default class SubstackApi {
  constructor({
                email = null,
                password = null,
                base_url = null,
                publication_url = null,
                auth_token = null,
                auth_legacy_token = null,
              }) {
    this.email = email;
    this.password = password;
    this.base_url = base_url || 'https://substack.com/api/v1';
    this.publication_url = new URL('api/v1', publication_url).toString();
    this.auth_cookie = `substack.sid=${auth_token}; connect.sid=${auth_legacy_token};`

    this.session = axios;
  }

  static handleResponse(response) {
    if (!(response.status >= 200 && response.status < 300)) {
      throw new Error(`SubstackAPIException: ${response.status} ${response.statusText}`);
    }

    try {
      return response.data;
    } catch (error) {
      throw new Error(`SubstackRequestException: Invalid Response: ${response.data}`);
    }
  }

  async login() {
    const url = `${this.base_url}/login`;

    const response = await this.session.post(url, {
      captcha_response: null,
      email: this.email,
      for_pub: '',
      password: this.password,
      redirect: '/',
    })

    this.cookies = response.headers['set-cookie']

    return SubstackApi.handleResponse(response)
  }

  async secondAttemptLogin() {
    const url = `${this.base_url}/login`;

    const headers = {};
    headers['Cookie'] = this.cookies;

    const response = await this.session.post(url, {
      captcha_response: null,
      email: this.email,
      for_pub: '',
      password: this.password,
      redirect: '/',
    }, {headers})

    this.auth_cookie = response.headers['set-cookie'].find(cookie => cookie.startsWith('substack.sid='))

    return SubstackApi.handleResponse(response)
  }

  async getSubscriberByFilters({filters}) {
    const url = `${this.publication_url}/subscriber-stats`;

    filters.order_by_desc_nulls_last = 'subscription_created_at'

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const limit = 100
    const subscribers = []
    let response;
    let offset = 0;

    do {
      const body = {
        filters,
        limit,
        offset
      }

      const api_response = await this.session.post(url, body, {headers})
      response = SubstackApi.handleResponse(api_response)

      subscribers.push(...response.subscribers)
      offset += limit
    } while (response.subscribers.length === limit)

    return subscribers
  }

  async createSubscriberSetForEmail(subscribers_ids) {
    const url = `${this.publication_url}/subscriber_set`;

    const body = {
      user_ids: subscribers_ids
    }

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const response = await this.session.post(url, body, {headers})
    return SubstackApi.handleResponse(response)
  }

  async getPublicationUsers() {
    const url = `${this.publication_url}/publication/users`;

    const response = await this.session.get(url)
    return SubstackApi.handleResponse(response)
  }

  async getPublicationSubscriberCount() {
    const url = `${this.publication_url}/publication_launch_checklist`;

    const response = await this.session.get(url)
    return SubstackApi.handleResponse(response)
  }

  async getPosts() {
    const url = `${this.base_url}/reader/posts`;

    const response = await this.session.get(url)
    return SubstackApi.handleResponse(response)
  }

  async getDrafts({query = null} = {}) {
    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const limit = 25
    const posts = []
    let response;
    let offset = 0;

    do {
      let url = `${this.publication_url}/post_management/drafts?&order_by=relevance&order_direction=desc&limit=${limit}&offset=${offset}`;
      if (query) url += `&query=${query}`;

      const api_response = await this.session.get(url, {headers})
      response = SubstackApi.handleResponse(api_response)

      posts.push(...response.posts)
      offset += limit
    } while (limit === response.posts.length)

    return posts
  }

  async getDraft(draft_id) {
    const url = `${this.publication_url}/drafts/${draft_id}`;

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const response = await this.session.get(url, {headers})

    return SubstackApi.handleResponse(response)
  }

  async deleteDraft(draftId) {
    const url = `${this.publication_url}/drafts/${draftId}`;

    const response = await this.session.delete(url)
    return SubstackApi.handleResponse(response)
  }

  async postDraft(body) {
    const url = `${this.publication_url}/drafts`;

    const headers = {};
    headers['Cookie'] = this.auth_cookie;
    const response = await this.session.post(url, body, {headers})
    return SubstackApi.handleResponse(response)
  }

  async prepublishDraft(draft) {
    const url = `${this.publication_url}/drafts/${draft}/prepublish`;

    const response = await this.session.get(url)
    return SubstackApi.handleResponse(response)
  }

  async publishDraft(draft_id, send = true, shareAutomatically = false) {
    const url = `${this.publication_url}/drafts/${draft_id}/publish`;

    const body = {
      send,
      share_automatically: shareAutomatically
    }

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const response = await this.session.post(url, body, {headers})
    return SubstackApi.handleResponse(response)
  }

  async scheduleDraft(draft_id, datetime) {
    await this.putDraft(draft_id)

    const url = `${this.publication_url}/drafts/${draft_id}/schedule`;

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const body = {
      share_automatically: false,
      should_send_email: true
    }

    const response = await this.session.post(url, body, {headers})
    const api_response = SubstackApi.handleResponse(response)

    await this.scheduleRelease(draft_id, datetime)
  }

  async putDraft(draft_id) {
    const url = `${this.publication_url}/drafts/${draft_id}`;

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const body = {
      audience: 'only_paid',
      section_chosen: true,
      should_send_email: true,
      should_send_free_preview: true,
    }

    const response = await this.session.put(url, body, {headers})
    return SubstackApi.handleResponse(response)
  }

  async scheduleRelease(draft_id, datetime) {
    const url = `${this.publication_url}/drafts/${draft_id}/scheduled_release`;

    const headers = {};
    headers['Cookie'] = this.auth_cookie;

    const body = {
      email_audience: 'only_paid',
      post_audience: 'only_paid',
      share_automatically: false,
      trigger_at: datetime,
    }

    const response = await this.session.post(url, body, {headers})
    return SubstackApi.handleResponse(response)
  }

  async unscheduleDraft(draft) {
    const url = `${this.publication_url}/drafts/${draft}/schedule`;

    const response = await this.session.post(url, {post_date: null})
    return SubstackApi.handleResponse(response)
  }

  async getCategories() {
    const url = `${this.base_url}/categories`;

    const response = await this.session.get(url)
    return SubstackApi.handleResponse(response)
  }

  async getCategory(categoryId, categoryType, page) {
    const url = `${this.base_url}/category/public/${categoryId}/${categoryType}`;

    const response = await this.session.get(url, {params: {page}})
    return SubstackApi.handleResponse(response)
  }

  async getSingleCategory(categoryId, categoryType, page = null, limit = null) {
    if (page !== null) {
      return this.getCategory(categoryId, categoryType, page);
    }

    let publications = [];
    let currentPage = 0;

    const fetchNextPage = () => {
      return this.getCategory(categoryId, categoryType, currentPage)
        .then(pageOutput => {
          publications = publications.concat(pageOutput.publications || []);
          currentPage += 1;

          if ((limit !== null && limit <= publications.length) || !pageOutput.more) {
            publications = publications.slice(0, limit);
            return {publications, more: false};
          }

          return fetchNextPage();
        });
    };

    return fetchNextPage();
  }

  async deleteAllDrafts() {
    let response = null;

    const fetchAndDeleteDrafts = () => {
      return this.getDrafts('draft', 0, 10)
        .then(drafts => {
          if (drafts.length === 0) {
            return response;
          }

          return Promise.all(drafts.map(draft => this.deleteDraft(draft.id)))
            .then(() => fetchAndDeleteDrafts());
        });
    };

    return fetchAndDeleteDrafts();
  }

  async getSections() {
    const url = `${this.publication_url}/subscriptions`;

    return this.session.get(url)
      .then(response => {
        const content = SubstackApi.handleResponse(response);
        const sections = content.publications
          .filter(p => p.hostname === this.publication_url)
          .map(p => p.sections);

        return sections[0];
      });
  }
}