import React, { useState, useCallback } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "@/lib/api";

interface VideoInfo {
  video_id: string;
  title: string;
  channel: string;
  thumbnail_url: string;
  available_languages: string[];
  original_url: string;
}

interface URLInputProps {
  onVideoInfoLoaded: (videoInfo: VideoInfo) => void;
  onLoading: (loading: boolean) => void;
  onError: (error: string) => void;
  isLoading?: boolean;
}

export default function URLInput({
  onVideoInfoLoaded,
  onLoading,
  onError,
  isLoading = false,
}: URLInputProps) {
  const [url, setUrl] = useState("");

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      if (!url.trim()) {
        onError("Please enter a YouTube URL");
        return;
      }

      onLoading(true);
      onError("");

      try {
        const response = await axios.post<VideoInfo>(API_ENDPOINTS.VIDEO_INFO, null, {
          params: { url: url.trim() },
        });

        onVideoInfoLoaded(response.data);
        setUrl("");
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.detail || "Failed to load video information";
        onError(errorMessage);
      } finally {
        onLoading(false);
      }
    },
    [url, onVideoInfoLoaded, onLoading, onError]
  );

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="space-y-4">
        <div>
          <label htmlFor="url-input" className="block text-sm font-medium text-gray-700 mb-2">
            YouTube URL
          </label>
          <input
            id="url-input"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            disabled={isLoading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            aria-describedby="url-help"
          />
          <p id="url-help" className="mt-1 text-sm text-gray-500">
            Supports: youtube.com/watch?v=..., youtu.be/..., youtube.com/shorts/...
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading || !url.trim()}
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? "Loading video info..." : "Continue"}
        </button>
      </div>
    </form>
  );
}
