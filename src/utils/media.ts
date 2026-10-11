export function getYouTubeId(url?: string | null): string | null {
  if (!url) return null;
  const match = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|shorts\/|watch\?v=|watch\?.+&v=))([\w-]{11})/);
  return match ? match[1] : null;
}

export function getVimeoId(url?: string | null): string | null {
  if (!url) return null;
  const match = url.match(/(?:vimeo\.com\/|player\.vimeo\.com\/video\/)(\d+)/);
  return match ? match[1] : null;
}

export function isDirectVideo(url?: string | null): boolean {
  if (!url) return false;
  return /\.(mp4|webm|ogg|mov)(\?.*)?$/i.test(url) || (url.startsWith('/images/') && /\.(mp4|webm|ogg|mov)/i.test(url));
}

export interface MediaInfo {
  youtubeId: string | null;
  vimeoId: string | null;
  embedUrl: string | null;
  isDirectVideo: boolean;
  coverImage: string | null;
  hasVideo: boolean;
  videoSrc: string | null;
}

export function resolveMedia(videoSrc?: string | null, imageSrc?: string | null): MediaInfo {
  const ytVideoId = getYouTubeId(videoSrc);
  const vimeoVideoId = getVimeoId(videoSrc);

  // Check if imageSrc itself was pasted as a YouTube URL
  const ytImageId = getYouTubeId(imageSrc);

  let coverImage = imageSrc || null;
  if (ytImageId) {
    coverImage = `https://img.youtube.com/vi/${ytImageId}/hqdefault.jpg`;
  } else if (!coverImage && ytVideoId) {
    // Fallback to YouTube thumbnail if no explicit cover image
    coverImage = `https://img.youtube.com/vi/${ytVideoId}/hqdefault.jpg`;
  }

  let embedUrl: string | null = null;
  if (ytVideoId) {
    embedUrl = `https://www.youtube.com/embed/${ytVideoId}?rel=0`;
  } else if (vimeoVideoId) {
    embedUrl = `https://player.vimeo.com/video/${vimeoVideoId}`;
  }

  const directVideo = isDirectVideo(videoSrc);
  const hasVideo = Boolean(embedUrl || directVideo);

  return {
    youtubeId: ytVideoId,
    vimeoId: vimeoVideoId,
    embedUrl,
    isDirectVideo: directVideo,
    coverImage,
    hasVideo,
    videoSrc: videoSrc || null,
  };
}
