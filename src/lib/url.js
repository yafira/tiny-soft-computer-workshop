// prefix a root-relative path with the site's base (/tiny)
export const p = (path) => import.meta.env.BASE_URL.replace(/\/$/, '') + path;
