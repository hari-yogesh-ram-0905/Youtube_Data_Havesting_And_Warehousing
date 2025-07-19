CREATE DATABASE Youtube;

USE Youtube;


SELECT * FROM channel;
SELECT * FROM playlist;
SELECT * FROM video;
SELECT * FROM comment;

SELECT * FROM channel 
WHERE Playlist_Id = 'UU8mfp2oMED6_AERJNmkoTjA';

SET SQL_SAFE_UPDATES = 0;

SELECT video_Id FROM video WHERE channel_Id = 'UCDSkjqkm5k0xv9ejdV2QlPQ';

-- delete comment details for particular channel_id
-- DELETE FROM comment WHERE video_Id IN (SELECT video_Id FROM video WHERE channel_Id = 'UCDSkjqkm5k0xv9ejdV2QlPQ');

-- delete video details for particular channel_id
-- DELETE FROM video WHERE channel_Id = 'UCDSkjqkm5k0xv9ejdV2QlPQ';

-- delete channel details for particular channel id
-- DELETE FROM channel WHERE channel_Id = "UCDSkjqkm5k0xv9ejdV2QlPQ";

-- delete playlist details by using particular channel id
-- DELETE FROM playlist WHERE channel_Id = "UCDSkjqkm5k0xv9ejdV2QlPQ";

-- DROP DATABASE Youtube;