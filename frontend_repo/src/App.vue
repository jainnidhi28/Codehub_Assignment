<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div class="logo">THE MOVIE DB</div>
          <nav>
            <ul class="nav-links">
              <li><a href="#">Movies</a></li>
              <li><a href="#">TV Shows</a></li>
              <li><a href="#">People</a></li>
              <li><a href="#">More</a></li>
            </ul>
          </nav>
          <div class="header-actions">
            <button v-if="!isLoggedIn" class="btn btn-secondary" @click="showLoginModal = true">Login</button>
            <button v-if="!isLoggedIn" class="btn btn-primary" @click="showSignupModal = true">Join TMDB</button>
            <div v-if="isLoggedIn" class="user-menu">
              <span class="username">{{ currentUser.username }}</span>
              <button class="btn btn-secondary" @click="logout">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      Loading movie details...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="movie" class="movie-content">
      <section class="hero">
        <div class="hero-background" :style="{ backgroundImage: `url(${movie.Poster})` }"></div>
        <div class="container">
          <div class="hero-content">
            <div class="poster-section">
              <img 
                :src="movie.Poster !== 'N/A' ? movie.Poster : '/placeholder-poster.jpg'" 
                :alt="movie.Title"
                class="movie-poster"
                @error="handleImageError"
              />
              <div class="streaming-info">
                <div class="streaming-logo">D+</div>
                <div>Now Streaming</div>
                <button class="btn btn-primary">Watch Now</button>
              </div>
            </div>

            <div class="movie-info">
              <div class="movie-header">
                <h1 class="movie-title">{{ movie.Title }} ({{ movie.Year }})</h1>
                <button 
                  v-if="movie.Title !== 'Guardians of the Galaxy Vol. 2'" 
                  class="back-home-btn" 
                  @click="goBackToHome"
                >
                  <span>🏠</span> Back to Home
                </button>
              </div>
              
              <div class="movie-meta">
                <span class="rating-badge">{{ movie.Rated || 'PG-13' }}</span>
                <span>{{ movie.Year }}</span>
                <span>•</span>
                <span>{{ movie.Runtime || '2h 17m' }}</span>
                <span>•</span>
                <span>{{ movie.Genre }}</span>
              </div>

              <div class="user-score">
                <div class="score-circle">
                  {{ calculateUserScore() }}%
                </div>
                <div>
                  <div>User Score</div>
                  <div style="font-size: 0.8rem; color: #cccccc;">{{ movie.imdbVotes }} votes</div>
                </div>
              </div>

              <div class="tagline">
                Anyone can save the galaxy once.
              </div>

              <div class="action-buttons">
                <button class="action-btn" :class="{ 'active': isInList }" @click="addToList">
                  <span>📋</span>
                  {{ isInList ? 'Listed' : 'List' }}
                </button>
                <button class="action-btn" :class="{ 'active': isLiked }" @click="toggleLike">
                  <span>{{ isLiked ? '❤' : '🤍' }}</span>
                  {{ isLiked ? 'Liked' : 'Like' }}
                </button>
                <button class="action-btn" :class="{ 'active': isBookmarked }" @click="toggleBookmark">
                  <span>{{ isBookmarked ? '🔖' : '📑' }}</span>
                  {{ isBookmarked ? 'Bookmarked' : 'Bookmark' }}
                </button>
                <button class="action-btn" :class="{ 'active': userRating > 0 }" @click="toggleRating">
                  <span>{{ userRating > 0 ? '⭐' : '☆' }}</span>
                  {{ userRating > 0 ? 'Rated' : 'Rate' }}
                </button>
                <button class="action-btn play-trailer" @click="openTrailerModal">
                  <span>🎬</span>
                  Play Trailer
                </button>
              </div>

              <div class="overview-section">
                <h3>Overview</h3>
                <p class="overview-text">{{ movie.Plot }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

             <section class="cast-crew">
               <div class="container">
                 <h3>{{ currentMovieTitle }} Cast</h3>
                 <div class="cast-text" v-if="currentMovieCast">
                   <div class="cast-category">
                     <h4>Main Characters</h4>
                     <p v-for="actor in currentMovieCast.main" :key="actor.name">
                       <strong>{{ actor.name }}</strong> as <em>{{ actor.role }}</em> - {{ actor.description }}
                     </p>
                   </div>
                   
                   <div class="cast-category">
                     <h4>Supporting Cast</h4>
                     <p v-for="actor in currentMovieCast.supporting" :key="actor.name">
                       <strong>{{ actor.name }}</strong> as <em>{{ actor.role }}</em> - {{ actor.description }}
                     </p>
                   </div>
                   
                   <div class="cast-category">
                     <h4>Behind the Scenes</h4>
                     <p v-for="person in currentMovieCast.behind" :key="person.name">
                       <strong>{{ person.name }}</strong> - {{ person.role }}
                     </p>
                   </div>
                 </div>
                 
                 <div class="cast-text" v-else>
                   <div class="cast-category">
                     <h4>Main Characters</h4>
                     <p><strong>Chris Pratt</strong> as <em>Peter Quill / Star-Lord</em> - The charismatic leader with a love for classic rock</p>
                     <p><strong>Zoe Saldaña</strong> as <em>Gamora</em> - The deadly assassin with a heart of gold</p>
                     <p><strong>Dave Bautista</strong> as <em>Drax the Destroyer</em> - The literal-minded warrior seeking vengeance</p>
                   </div>
                   
                   <div class="cast-category">
                     <h4>Voice Actors</h4>
                     <p><strong>Vin Diesel</strong> as <em>Groot</em> - The lovable tree-like creature (voiced with just three words!)</p>
                     <p><strong>Bradley Cooper</strong> as <em>Rocket</em> - The genetically engineered raccoon with attitude</p>
                   </div>
                   
                   <div class="cast-category">
                     <h4>Supporting Cast</h4>
                     <p><strong>Karen Gillan</strong> as <em>Nebula</em> - Gamora's cybernetic sister</p>
                     <p><strong>Michael Rooker</strong> as <em>Yondu Udonta</em> - The blue-skinned Ravager captain</p>
                     <p><strong>Sean Gunn</strong> as <em>Kraglin</em> - Yondu's loyal first mate</p>
                     <p><strong>Pom Klementieff</strong> as <em>Mantis</em> - The empathic alien with antennae</p>
                   </div>
                   
                   <div class="cast-category">
                     <h4>Behind the Scenes</h4>
                     <p><strong>James Gunn</strong> - Director & Writer</p>
                     <p><strong>Kevin Feige</strong> - Producer</p>
                   </div>
                 </div>
               </div>
             </section>

      <section class="social-section">
        <div class="container">
          <div class="social-tabs">
            <button class="tab-btn" :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">Reviews</button>
            <button class="tab-btn" :class="{ active: activeTab === 'discussions' }" @click="activeTab = 'discussions'">Discussions</button>
          </div>
          
          <div v-if="activeTab === 'reviews'" class="reviews-content">
            <!-- Add Review Form -->
            <div class="add-review-form">
              <h4>Add Your Review</h4>
              <form @submit.prevent="submitReview">
                <div class="form-row">
                  <div class="form-group">
                    <label>Your Name</label>
                    <input type="text" v-model="newReview.author" required />
                  </div>
                  <div class="form-group">
                    <label>Rating (%)</label>
                    <input type="number" v-model="newReview.rating" min="0" max="100" required />
                  </div>
                </div>
                <div class="form-group">
                  <label>Your Review</label>
                  <textarea v-model="newReview.text" rows="4" placeholder="Share your thoughts about this movie..." required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Submit Review</button>
              </form>
            </div>
            
            <!-- Reviews List -->
            <div class="reviews-list">
              <h4>All Reviews</h4>
              <div class="review-item" v-for="review in currentReviews.length > 0 ? currentReviews : reviews" :key="review.id">
                <div class="review-header">
                  <div class="reviewer-info">
                    <div class="reviewer-name">{{ review.author }}</div>
                    <div class="review-date">{{ review.date }}</div>
                  </div>
                  <div class="review-rating">{{ review.rating }}%</div>
                </div>
                <div class="review-text">{{ review.text }}</div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'discussions'" class="discussions-content">
            <!-- Add Discussion Form -->
            <div class="add-discussion-form">
              <h4>Start a Discussion</h4>
              <form @submit.prevent="submitDiscussion">
                <div class="form-row">
                  <div class="form-group">
                    <label>Your Name</label>
                    <input type="text" v-model="newDiscussion.author" required />
                  </div>
                  <div class="form-group">
                    <label>Discussion Title</label>
                    <input type="text" v-model="newDiscussion.title" placeholder="Enter discussion title..." required />
                  </div>
                </div>
                <div class="form-group">
                  <label>Discussion Content</label>
                  <textarea v-model="newDiscussion.preview" rows="4" placeholder="Share your thoughts and start a discussion..." required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Start Discussion</button>
              </form>
            </div>
            
            <!-- Discussions List -->
            <div class="discussions-list">
              <h4>All Discussions</h4>
              <div class="discussion-item" v-for="discussion in currentDiscussions.length > 0 ? currentDiscussions : discussions" :key="discussion.id">
                <div class="discussion-header">
                  <div class="discussion-title">{{ discussion.title }}</div>
                  <div class="discussion-meta">
                    <span>by {{ discussion.author }}</span>
                    <span>{{ discussion.date }}</span>
                    <span>{{ discussion.replies }} replies</span>
                  </div>
                </div>
                <div class="discussion-preview">{{ discussion.preview }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="smart-recommendations">
        <div class="container">
          <div class="recommendations-header">
            <h3>Smart Recommendations</h3>
            <p>Based on your taste and this movie's profile</p>
            <div class="recommendations-actions">
              <button class="btn btn-secondary" @click="refreshRecommendations">Get More</button>
              <button v-if="smartRecommendations.length > 3" class="btn btn-secondary" @click="showLessRecommendations">Show Less</button>
            </div>
          </div>
          <div class="recommendations-grid">
            <div 
              v-for="(rec, index) in smartRecommendations" 
              :key="index" 
              class="recommendation-card"
              @click="selectRecommendation(rec)"
            >
              <div class="rec-poster">
                <img :src="rec.poster" :alt="rec.title" />
                <div class="rec-overlay">
                  <button class="btn btn-primary">View Details</button>
                </div>
              </div>
              <div class="rec-info">
                <h4>{{ rec.title }}</h4>
                <div class="rec-meta">
                  <span class="rec-year">{{ rec.year }}</span>
                  <span class="rec-rating">{{ rec.rating }}</span>
                </div>
                <p class="rec-reason">{{ rec.reason }}</p>
                <div class="rec-match">
                  <div class="match-bar">
                    <div class="match-fill" :style="{ width: rec.match + '%' }"></div>
                  </div>
                  <span>{{ rec.match }}% Match</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="enhanced-features">
        <div class="container">
          <h3>Enhanced Features</h3>
          <div class="features-grid">
            <div class="feature-card">
              <h4>Interactive Trailer</h4>
              <p>Click to watch the official trailer with enhanced controls</p>
              <button class="btn btn-primary" @click="openTrailerModal">Watch Trailer</button>
            </div>
            <div class="feature-card">
              <h4>Mobile Optimized</h4>
              <p>Perfect viewing experience on all devices</p>
              <div class="device-icons">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div class="feature-card">
              <h4>Smart Recommendations</h4>
              <p>Get personalized movie suggestions based on your taste</p>
              <button class="btn btn-secondary" @click="refreshRecommendations">Get More</button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div v-if="showTrailerModal" class="modal-overlay" @click="closeTrailerModal">
      <div class="trailer-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ movie.Title }} - Official Trailer</h3>
          <button class="close-btn" @click="closeTrailerModal">×</button>
        </div>
        <div class="trailer-container">
          <div class="trailer-placeholder">
            <div class="trailer-controls">
              <button class="control-btn play-btn" @click="playTrailer">
                <span></span> Play Trailer
              </button>
              <button class="control-btn quality-btn" @click="toggleQuality">
                <span></span> HD
              </button>
              <button class="control-btn fullscreen-btn" @click="toggleFullscreen">
                <span></span> Fullscreen
              </button>
            </div>
            <div class="trailer-info">
              <p>Experience the epic adventure with enhanced controls</p>
              <div class="trailer-stats">
                <span>2.5M views</span>
                <span>4.8/5 rating</span>
                <span>2:34 duration</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeTrailerModal">Close</button>
          <button class="btn btn-primary" @click="addToWatchlist">Add to Watchlist</button>
        </div>
      </div>
    </div>

    <div v-if="showLoginModal" class="modal-overlay" @click="showLoginModal = false">
      <div class="auth-modal" @click.stop>
        <div class="modal-header">
          <h3>Login to TMDB</h3>
          <button class="close-btn" @click="showLoginModal = false">×</button>
        </div>
        <div class="auth-content">
          <form @submit.prevent="login">
            <div class="form-group">
              <label>Username</label>
              <input type="text" v-model="loginForm.username" required />
            </div>
            <div class="form-group">
              <label>Password</label>
              <input type="password" v-model="loginForm.password" required />
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showSignupModal" class="modal-overlay" @click="showSignupModal = false">
      <div class="auth-modal" @click.stop>
        <div class="modal-header">
          <h3>Join TMDB</h3>
          <button class="close-btn" @click="showSignupModal = false">×</button>
        </div>
        <div class="auth-content">
          <form @submit.prevent="signup">
            <div class="form-group">
              <label>Username</label>
              <input type="text" v-model="signupForm.username" required />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="signupForm.email" required />
            </div>
            <div class="form-group">
              <label>Password</label>
              <input type="password" v-model="signupForm.password" required />
            </div>
            <button type="submit" class="btn btn-primary">Sign Up</button>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showRatingModal" class="modal-overlay" @click="showRatingModal = false">
      <div class="rating-modal" @click.stop>
        <div class="modal-header">
          <h3>Rate {{ movie.Title }}</h3>
          <button class="close-btn" @click="showRatingModal = false">×</button>
        </div>
        <div class="rating-content">
          <div class="stars">
            <span 
              v-for="star in 10" 
              :key="star"
              class="star"
              :class="{ active: star <= userRating }"
              @click="userRating = star"
            ></span>
          </div>
          <div class="rating-text">{{ userRating }}/10</div>
          <button class="btn btn-primary" @click="submitRating">Submit Rating</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      movie: null,
      loading: true,
      error: null,
      showTrailerModal: false,
      showLoginModal: false,
      showSignupModal: false,
      showRatingModal: false,
      activeTab: 'reviews',
      reviews: [
        { id: 1, author: 'CinemaSerf', date: 'June 3, 2024', rating: 70, text: 'Oh well, they had to try I suppose - and as sequels go, this isn\'t the worst - but it\'s a far cry from the first one. Chris Pratt still has a cheeky charm as \'Peter Quill\' but somehow the writing and humour in this are not so relaxed and spontaneous...' },
        { id: 2, author: 'MovieLover', date: 'June 2, 2024', rating: 85, text: 'The action sequences are top-notch, and the chemistry between the characters is undeniable. The plot twists are well-executed, and the ending is satisfying.' },
        { id: 3, author: 'CriticMan', date: 'June 1, 2024', rating: 90, text: 'A true masterpiece. The visuals, the sound, the story, everything is perfect. The movie is a cinematic experience that will leave you breathless.' },
      ],
      discussions: [
        { id: 1, title: 'Guardians of the Galaxy Vol. 2 - Best Moments', author: 'MovieFanatic', date: 'June 4, 2024', replies: 15, preview: 'What are your favorite moments from Guardians of the Galaxy Vol. 2? Share them here!' },
        { id: 2, title: 'Thor: Ragnarok - Movie Discussion', author: 'ComicBookNerd', date: 'June 3, 2024', replies: 10, preview: 'Let\'s discuss Thor: Ragnarok. What did you think of the new Thor? The humor? The action?' },
        { id: 3, author: 'MovieCritic', date: 'June 2, 2024', replies: 5, preview: 'Is Guardians of the Galaxy Vol. 2 better than the first one? Let\'s debate!' },
      ],
      currentReviews: [],
      currentDiscussions: [],

      smartRecommendations: [
        {
          title: 'Avengers: Infinity War',
          year: '2018',
          rating: '8.4/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_SX300.jpg',
          reason: 'Similar superhero ensemble with cosmic scale',
          match: 94,
          cast: {
            main: [
              { name: 'Robert Downey Jr.', role: 'Tony Stark / Iron Man', description: 'The genius billionaire facing his greatest challenge' },
              { name: 'Chris Evans', role: 'Steve Rogers / Captain America', description: 'The first Avenger leading the resistance' },
              { name: 'Mark Ruffalo', role: 'Bruce Banner / Hulk', description: 'The scientist struggling with his green side' },
              { name: 'Chris Hemsworth', role: 'Thor', description: 'The God of Thunder seeking revenge' },
              { name: 'Scarlett Johansson', role: 'Natasha Romanoff / Black Widow', description: 'The spy fighting for humanity' },
              { name: 'Josh Brolin', role: 'Thanos', description: 'The Mad Titan seeking the Infinity Stones' }
            ],
            supporting: [
              { name: 'Tom Holland', role: 'Peter Parker / Spider-Man', description: 'The young hero caught in cosmic war' },
              { name: 'Chadwick Boseman', role: 'T\'Challa / Black Panther', description: 'The king of Wakanda defending his people' },
              { name: 'Benedict Cumberbatch', role: 'Doctor Strange', description: 'The sorcerer who sees all possibilities' }
            ],
            behind: [
              { name: 'Anthony Russo', role: 'Director' },
              { name: 'Joe Russo', role: 'Director' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'MarvelFan', date: 'May 15, 2018', rating: 95, text: 'The culmination of 10 years of Marvel storytelling. Thanos is the perfect villain, and the ending is absolutely devastating. This is what superhero movies should be.' },
            { id: 2, author: 'CinemaCritic', date: 'May 14, 2018', rating: 88, text: 'The Russo brothers deliver an epic that balances humor, action, and emotion perfectly. The character interactions are gold, especially between Iron Man and Doctor Strange.' },
            { id: 3, author: 'MovieBuff', date: 'May 13, 2018', rating: 92, text: 'Incredible visual effects and a story that actually has consequences. The way it sets up the next phase is masterful. Can\'t wait for the sequel!' }
          ],
          discussions: [
            { id: 1, title: 'Infinity War - The Snap Discussion', author: 'ThanosFan', date: 'May 16, 2018', replies: 45, preview: 'What did you think of the snap? Which character deaths hit you the hardest?' },
            { id: 2, title: 'Iron Man vs Thanos - Best Fight Scene?', author: 'ActionLover', date: 'May 15, 2018', replies: 32, preview: 'The fight on Titan is absolutely incredible. The coordination between all the heroes is perfect!' },
            { id: 3, title: 'Infinity Stones - Power Ranking', author: 'MarvelNerd', date: 'May 14, 2018', replies: 28, preview: 'Let\'s rank the Infinity Stones by their power and importance in the MCU.' }
          ]
        },
        {
          title: 'Thor: Ragnarok',
          year: '2017',
          rating: '7.9/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_SX300.jpg',
          reason: 'Same director, similar humor and action',
          match: 89,
          cast: {
            main: [
              { name: 'Chris Hemsworth', role: 'Thor', description: 'The God of Thunder who loses his hammer' },
              { name: 'Tom Hiddleston', role: 'Loki', description: 'The God of Mischief and Thor\'s brother' },
              { name: 'Cate Blanchett', role: 'Hela', description: 'The Goddess of Death and Thor\'s sister' },
              { name: 'Tessa Thompson', role: 'Valkyrie', description: 'The fierce warrior and former Valkyrie' },
              { name: 'Mark Ruffalo', role: 'Bruce Banner / Hulk', description: 'The green giant stuck in Hulk form' },
              { name: 'Jeff Goldblum', role: 'Grandmaster', description: 'The eccentric ruler of Sakaar' }
            ],
            supporting: [
              { name: 'Karl Urban', role: 'Skurge', description: 'The executioner who serves Hela' },
              { name: 'Anthony Hopkins', role: 'Odin', description: 'The Allfather and Thor\'s father' },
              { name: 'Idris Elba', role: 'Heimdall', description: 'The all-seeing guardian of the Bifrost' }
            ],
            behind: [
              { name: 'Taika Waititi', role: 'Director' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'ThorFan', date: 'November 8, 2017', rating: 92, text: 'Taika Waititi completely reinvented Thor! The humor is perfect, the action is incredible, and the visual design of Sakaar is stunning. This is the Thor movie we needed.' },
            { id: 2, author: 'ComedyLover', date: 'November 7, 2017', rating: 89, text: 'The balance of comedy and action is masterful. Jeff Goldblum as the Grandmaster is pure gold, and the Hulk-Thor dynamic is hilarious.' },
            { id: 3, author: 'ActionFan', date: 'November 6, 2017', rating: 87, text: 'The fight scenes are epic, especially the gladiator battle. The soundtrack with Led Zeppelin is perfect. This movie is pure entertainment!' }
          ],
          discussions: [
            { id: 1, title: 'Thor: Ragnarok - Best Comedy Moments', author: 'HumorFan', date: 'November 9, 2017', replies: 38, preview: 'What\'s your favorite funny moment? The hammer scene? The Hulk-Thor interactions?' },
            { id: 2, title: 'Sakaar Design - Visual Masterpiece', author: 'ArtLover', date: 'November 8, 2017', replies: 25, preview: 'The visual design of Sakaar is incredible. The colors, the architecture, everything is so unique!' },
            { id: 3, title: 'Hela vs Thor - Epic Battle', author: 'BattleFan', date: 'November 7, 2017', replies: 31, preview: 'Cate Blanchett as Hela is terrifying and powerful. The final battle is absolutely epic!' }
          ]
        },
        {
          title: 'Captain Marvel',
          year: '2019',
          rating: '6.8/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BMTE0YWFmOTMtYTU2ZS00ZTIxLWE3OTEtYTNiYzBkZjViZThiXkEyXkFqcGdeQXVyODMzMzQ4OTI@._V1_SX300.jpg',
          reason: 'Space adventure with strong female lead',
          match: 82,
          cast: {
            main: [
              { name: 'Brie Larson', role: 'Carol Danvers / Captain Marvel', description: 'The powerful Kree warrior discovering her past' },
              { name: 'Samuel L. Jackson', role: 'Nick Fury', description: 'The SHIELD agent with both eyes' },
              { name: 'Ben Mendelsohn', role: 'Talos', description: 'The Skrull leader seeking a new home' },
              { name: 'Jude Law', role: 'Yon-Rogg', description: 'The Kree commander and Carol\'s mentor' },
              { name: 'Annette Bening', role: 'Mar-Vell / Supreme Intelligence', description: 'The Kree scientist who changed everything' },
              { name: 'Lashana Lynch', role: 'Maria Rambeau', description: 'Carol\'s best friend and fellow pilot' }
            ],
            supporting: [
              { name: 'Clark Gregg', role: 'Phil Coulson', description: 'The young SHIELD agent' },
              { name: 'Lee Pace', role: 'Ronan the Accuser', description: 'The Kree fanatic' },
              { name: 'Djimon Hounsou', role: 'Korath', description: 'The Kree warrior' }
            ],
            behind: [
              { name: 'Anna Boden', role: 'Director' },
              { name: 'Ryan Fleck', role: 'Director' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'MarvelGirl', date: 'March 12, 2019', rating: 85, text: 'Brie Larson is perfect as Captain Marvel! The 90s setting is nostalgic, and the Skrull twist is brilliant. This origin story is exactly what we needed.' },
            { id: 2, author: 'SpaceFan', date: 'March 11, 2019', rating: 82, text: 'The cosmic elements are great, and the friendship between Carol and Maria is heartwarming. The action sequences are spectacular!' },
            { id: 3, author: 'FuryFan', date: 'March 10, 2019', rating: 88, text: 'Young Nick Fury is amazing! The cat Goose steals every scene. The movie perfectly sets up the character for Endgame.' }
          ],
          discussions: [
            { id: 1, title: 'Captain Marvel - Female Hero Discussion', author: 'HeroFan', date: 'March 13, 2019', replies: 52, preview: 'What do you think about Marvel\'s first female-led superhero movie? How does it compare to Wonder Woman?' },
            { id: 2, title: 'The Skrull Twist - Brilliant or Confusing?', author: 'PlotLover', date: 'March 12, 2019', replies: 41, preview: 'The Skrull reveal was unexpected! Did you see it coming? How does it change the MCU?' },
            { id: 3, title: '90s Nostalgia - Perfect Setting', author: 'RetroFan', date: 'March 11, 2019', replies: 29, preview: 'The 90s setting is perfect! The Blockbuster scene, the music, everything is so nostalgic!' }
          ]
        },

      ],
      isLoggedIn: false,
      currentUser: { username: 'Guest' },
      loginForm: { username: '', password: '' },
      signupForm: { username: '', email: '', password: '' },
              userRating: 0,
        watchlist: ['tt3896198'],
      currentMovieTitle: 'Guardians of the Galaxy Vol. 2',
      currentMovieCast: null,
      isInList: false,
      isLiked: false,
      isBookmarked: false,
      loginForm: { username: '', password: '' },
      signupForm: { username: '', email: '', password: '' },
      newReview: { author: '', rating: '', text: '' },
      newDiscussion: { author: '', title: '', preview: '' },
      createdUsers: []
    }
  },
  async mounted() {
    await this.fetchMovieData()
  },
  methods: {
    async fetchMovieData() {
      try {
        this.loading = true
        this.error = null
        
        const response = await axios.get('http://www.omdbapi.com/?i=tt3896198&apikey=d2132124')
        
        if (response.data.Response === 'True') {
          this.movie = response.data
        } else {
          this.error = 'Failed to load movie data'
        }
      } catch (err) {
        this.error = 'Error loading movie data: ' + err.message
      } finally {
        this.loading = false
      }
    },
    
    calculateUserScore() {
      if (this.movie && this.movie.imdbRating) {
        return Math.round(parseFloat(this.movie.imdbRating) * 10)
      }
      return 76
    },
    
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/300x450/1a1d29/ffffff?text=No+Poster'
    },

    handleCastImageError(event) {
      event.target.src = 'https://via.placeholder.com/150x225/1a1d29/ffffff?text=No+Photo'
    },

    selectRecommendation(rec) {
      this.showNavigationFeedback(rec.title)
      
      setTimeout(() => {
        this.loadMovieData(rec)
      }, 1500)
    },

    getMovieId(title) {
      const movieMap = {
        'Avengers: Infinity War': 'tt4154756',
        'Thor: Ragnarok': 'tt3501632',
        'Captain Marvel': 'tt4154664',
        'Ant-Man and the Wasp': 'tt5095030',
        'Black Panther': 'tt1825683',
        'Spider-Man: Homecoming': 'tt2250912'
      }
              return movieMap[title] || 'tt3896198'
    },

    async loadMovieData(rec) {
      try {
        this.loading = true
        
        const mockMovieData = {
          'Avengers: Infinity War': {
            Title: 'Avengers: Infinity War',
            Year: '2018',
            Rated: 'PG-13',
            Runtime: '149 min',
            Genre: 'Action, Adventure, Drama',
            Director: 'Anthony Russo, Joe Russo',
            Plot: 'The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.',
            Poster: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_SX300.jpg',
            imdbRating: '8.4',
            imdbVotes: '1,000,000+'
          },
          'Thor: Ragnarok': {
            Title: 'Thor: Ragnarok',
            Year: '2017',
            Rated: 'PG-13',
            Runtime: '130 min',
            Genre: 'Action, Adventure, Comedy',
            Director: 'Taika Waititi',
            Plot: 'Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarök, the destruction of his world, at the hands of the powerful and ruthless villain Hela.',
            Poster: 'https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_SX300.jpg',
            imdbRating: '7.9',
            imdbVotes: '700,000+'
          },
          'Captain Marvel': {
            Title: 'Captain Marvel',
            Year: '2019',
            Rated: 'PG-13',
            Runtime: '123 min',
            Genre: 'Action, Adventure, Sci-Fi',
            Director: 'Anna Boden, Ryan Fleck',
            Plot: 'Carol Danvers becomes one of the universe\'s most powerful heroes when Earth is caught in the middle of a galactic war between two alien races.',
            Poster: 'https://m.media-amazon.com/images/M/MV5BMTE0YWFmOTMtYTU2ZS00ZTIxLWE3OTEtYTNiYzBkZjViZThiXkEyXkFqcGdeQXVyODMzMzQ4OTI@._V1_SX300.jpg',
            imdbRating: '6.8',
            imdbVotes: '500,000+'
          },
          'Ant-Man and the Wasp': {
            Title: 'Ant-Man and the Wasp',
            Year: '2018',
            Rated: 'PG-13',
            Runtime: '118 min',
            Genre: 'Action, Adventure, Comedy',
            Director: 'Peyton Reed',
            Plot: 'As Scott Lang balances being both a superhero and a father, Hope van Dyne and Dr. Hank Pym present an urgent new mission that finds the Ant-Man fighting alongside The Wasp to uncover secrets from their past.',
            Poster: 'https://m.media-amazon.com/images/M/MV5BYjcyYTk0N2YtMzc4ZC00Y2E0OWE0YzY1NWY5OTI4NTY4OTYxXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            imdbRating: '7.0',
            imdbVotes: '400,000+'
          }
        }
        
        this.movie = mockMovieData[rec.title] || this.movie
        
        this.currentMovieTitle = rec.title
        this.currentMovieCast = rec.cast
        this.currentReviews = rec.reviews || []
        this.currentDiscussions = rec.discussions || []
        
        document.title = `${rec.title} (${rec.year}) - Movie Details`
        
        window.scrollTo({ top: 0, behavior: 'smooth' })
        
        this.loading = false
        
        this.showSuccessMessage(`Successfully loaded ${rec.title}!`)
        
      } catch (err) {
        this.error = 'Error loading movie data'
        this.loading = false
      }
    },

    showNavigationFeedback(title) {
      const notification = document.createElement('div')
      notification.className = 'navigation-notification'
      notification.innerHTML = `
        <div class="notification-content">
          <span>Loading ${title}...</span>
          <div class="loading-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      `
      document.body.appendChild(notification)
      
      setTimeout(() => {
        notification.remove()
      }, 1500)
    },

    showSuccessMessage(message) {
      const successNotification = document.createElement('div')
      successNotification.className = 'success-notification'
      successNotification.innerHTML = `
        <div class="success-content">
          <span>${message}</span>
        </div>
      `
      document.body.appendChild(successNotification)
      
      setTimeout(() => {
        successNotification.remove()
      }, 3000)
    },

    refreshRecommendations() {
      const additionalRecommendations = [
        {
          title: 'Black Panther',
          year: '2018',
          rating: '7.3/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BMTg1MTY2MjYzNV5BMl5BanBnXkFtZTgwMTc4NTMwNDI@._V1_SX300.jpg',
          reason: 'Cultural phenomenon with powerful themes',
          match: 85,
          cast: {
            main: [
              { name: 'Chadwick Boseman', role: 'T\'Challa / Black Panther', description: 'The noble king of Wakanda' },
              { name: 'Michael B. Jordan', role: 'Erik Killmonger', description: 'The vengeful warrior seeking justice' },
              { name: 'Lupita Nyong\'o', role: 'Nakia', description: 'The fierce spy and T\'Challa\'s love interest' },
              { name: 'Danai Gurira', role: 'Okoye', description: 'The loyal general of the Dora Milaje' },
              { name: 'Letitia Wright', role: 'Shuri', description: 'The brilliant princess and tech genius' },
              { name: 'Martin Freeman', role: 'Everett K. Ross', description: 'The CIA agent caught in the middle' }
            ],
            supporting: [
              { name: 'Angela Bassett', role: 'Ramonda', description: 'The wise queen mother' },
              { name: 'Forest Whitaker', role: 'Zuri', description: 'The spiritual advisor to the throne' },
              { name: 'Andy Serkis', role: 'Ulysses Klaue', description: 'The arms dealer and Wakanda\'s enemy' }
            ],
            behind: [
              { name: 'Ryan Coogler', role: 'Director & Writer' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'WakandaFan', date: 'February 16, 2018', rating: 96, text: 'A masterpiece that transcends the superhero genre. The cultural significance, the performances, the world-building - everything is perfect.' },
            { id: 2, author: 'CinemaCritic', date: 'February 15, 2018', rating: 92, text: 'Ryan Coogler delivers a powerful story about identity, heritage, and responsibility. The action sequences are breathtaking.' },
            { id: 3, author: 'MarvelLover', date: 'February 14, 2018', rating: 94, text: 'Chadwick Boseman is regal and powerful. The world of Wakanda is beautifully realized. This is what representation looks like.' }
          ],
          discussions: [
            { id: 1, title: 'Wakanda Forever - Cultural Impact', author: 'CultureFan', date: 'February 17, 2018', replies: 67, preview: 'How has Black Panther changed the landscape of superhero movies? The cultural impact is undeniable!' },
            { id: 2, title: 'Killmonger - Best MCU Villain?', author: 'VillainFan', date: 'February 16, 2018', replies: 54, preview: 'Michael B. Jordan\'s Killmonger is complex and sympathetic. Is he the best villain in the MCU?' },
            { id: 3, title: 'Wakanda Technology - Vibranium Wonders', author: 'TechFan', date: 'February 15, 2018', replies: 43, preview: 'The technology in Wakanda is incredible! What\'s your favorite piece of Wakandan tech?' }
          ]
        },
        {
          title: 'Spider-Man: Homecoming',
          year: '2017',
          rating: '7.4/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BNTk4ODQ1MzgzNl5BMl5BanBnXkFtZTgwMTMyMzM4MTI@._V1_SX300.jpg',
          reason: 'Coming-of-age superhero story',
          match: 82,
          cast: {
            main: [
              { name: 'Tom Holland', role: 'Peter Parker / Spider-Man', description: 'The young hero learning to balance school and superheroics' },
              { name: 'Michael Keaton', role: 'Adrian Toomes / Vulture', description: 'The blue-collar villain with a personal grudge' },
              { name: 'Robert Downey Jr.', role: 'Tony Stark / Iron Man', description: 'The mentor figure and Peter\'s reluctant guide' },
              { name: 'Marisa Tomei', role: 'May Parker', description: 'Peter\'s loving and protective aunt' },
              { name: 'Jon Favreau', role: 'Happy Hogan', description: 'Tony\'s bodyguard and Peter\'s reluctant babysitter' },
              { name: 'Zendaya', role: 'Michelle Jones', description: 'The intelligent and mysterious classmate' }
            ],
            supporting: [
              { name: 'Jacob Batalon', role: 'Ned Leeds', description: 'Peter\'s best friend and guy in the chair' },
              { name: 'Laura Harrier', role: 'Liz Allan', description: 'Peter\'s crush and the Vulture\'s daughter' },
              { name: 'Tony Revolori', role: 'Flash Thompson', description: 'Peter\'s rival and school bully' }
            ],
            behind: [
              { name: 'Jon Watts', role: 'Director' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'SpideyFan', date: 'July 7, 2017', rating: 89, text: 'Tom Holland is the perfect Spider-Man! The high school setting feels authentic, and the Vulture is a great villain with personal stakes.' },
            { id: 2, author: 'MarvelFan', date: 'July 6, 2017', rating: 87, text: 'The balance of humor, action, and heart is perfect. The relationship with Tony Stark adds depth, and the stakes feel real.' },
            { id: 3, author: 'TeenMovieFan', date: 'July 5, 2017', rating: 85, text: 'Finally, a superhero movie that captures the awkwardness of being a teenager. The high school scenes are hilarious and relatable!' }
          ],
          discussions: [
            { id: 1, title: 'Best Spider-Man Movie?', author: 'SpideyLover', date: 'July 8, 2017', replies: 48, preview: 'How does Homecoming compare to the other Spider-Man movies? Is this the best one yet?' },
            { id: 2, title: 'Vulture Twist - Did You See It Coming?', author: 'PlotFan', date: 'July 7, 2017', replies: 39, preview: 'The Vulture reveal was shocking! Did anyone predict that twist? How does it change the story?' },
            { id: 3, title: 'High School vs Superhero Life', author: 'TeenFan', date: 'July 6, 2017', replies: 35, preview: 'The balance between school life and superhero life is perfect. Which scenes resonated with you most?' }
          ]
        },
        {
          title: 'Doctor Strange',
          year: '2016',
          rating: '7.5/10',
          poster: 'https://m.media-amazon.com/images/M/MV5BNjgwNzAzNjk1Nl5BMl5BanBnXkFtZTgwMzQ2NjI1OTE@._V1_SX300.jpg',
          reason: 'Mind-bending visual effects and magic',
          match: 79,
          cast: {
            main: [
              { name: 'Benedict Cumberbatch', role: 'Stephen Strange', description: 'The brilliant neurosurgeon turned sorcerer' },
              { name: 'Chiwetel Ejiofor', role: 'Karl Mordo', description: 'The disciplined sorcerer and Strange\'s mentor' },
              { name: 'Rachel McAdams', role: 'Christine Palmer', description: 'The emergency surgeon and Strange\'s former lover' },
              { name: 'Benedict Wong', role: 'Wong', description: 'The librarian and guardian of ancient texts' },
              { name: 'Mads Mikkelsen', role: 'Kaecilius', description: 'The rogue sorcerer seeking eternal life' },
              { name: 'Tilda Swinton', role: 'The Ancient One', description: 'The mysterious master of the mystic arts' }
            ],
            supporting: [
              { name: 'Michael Stuhlbarg', role: 'Nicodemus West', description: 'The rival surgeon and Strange\'s colleague' },
              { name: 'Benjamin Bratt', role: 'Jonathan Pangborn', description: 'The paralyzed man who found healing' },
              { name: 'Scott Adkins', role: 'Lucian', description: 'One of Kaecilius\' zealots' }
            ],
            behind: [
              { name: 'Scott Derrickson', role: 'Director' },
              { name: 'Kevin Feige', role: 'Producer' }
            ]
          },
          reviews: [
            { id: 1, author: 'MagicFan', date: 'November 4, 2016', rating: 88, text: 'The visual effects are absolutely mind-blowing! The Inception-style city folding scenes are revolutionary for superhero movies.' },
            { id: 2, author: 'CumberbatchFan', date: 'November 3, 2016', rating: 85, text: 'Benedict Cumberbatch is perfect as Doctor Strange. The character arc from arrogant surgeon to humble sorcerer is compelling.' },
            { id: 3, author: 'VisualFan', date: 'November 2, 2016', rating: 87, text: 'The mystical elements are beautifully realized. The Mirror Dimension and the Eye of Agamotto are incredible concepts!' }
          ],
          discussions: [
            { id: 1, title: 'Best Visual Effects in MCU?', author: 'VFXFan', date: 'November 5, 2016', replies: 52, preview: 'The visual effects in Doctor Strange are incredible! Are they the best in the entire MCU?' },
            { id: 2, title: 'Mystic Arts - Magic System', author: 'MagicLover', date: 'November 4, 2016', replies: 41, preview: 'The magic system in Doctor Strange is fascinating. How does it work? What are the rules?' },
            { id: 3, title: 'Dormammu - Time Loop Battle', author: 'BattleFan', date: 'November 3, 2016', replies: 38, preview: 'The final battle with Dormammu is unique! The time loop concept is brilliant. What did you think?' }
          ]
        }
      ]
      
      // Add the new recommendations to the existing ones
      this.smartRecommendations = [...this.smartRecommendations, ...additionalRecommendations]
    },

    showLessRecommendations() {
      this.smartRecommendations = this.smartRecommendations.slice(0, 3)
    },

    openTrailerModal() {
      this.showTrailerModal = true
      document.body.style.overflow = 'hidden'
    },

    closeTrailerModal() {
      this.showTrailerModal = false
      document.body.style.overflow = 'auto'
    },

    playTrailer() {
              alert('Trailer would start playing with enhanced controls:\n\n• HD quality\n• Custom playback speed\n• Interactive chapters\n• Picture-in-picture mode')
    },

    toggleQuality() {
              alert('Quality options:\n\n• 4K Ultra HD\n• 1080p HD\n• 720p HD\n• 480p SD')
    },

    toggleFullscreen() {
      alert('⛶ Fullscreen mode activated with:\n\n• Immersive viewing\n• Auto-hide controls\n• Gesture support')
    },

    addToWatchlist() {
              alert('Added to watchlist!\n\nYou\'ll be notified when the movie is available to stream.')
      this.closeTrailerModal()
    },

    goBackToHome() {
      this.loading = true;
      this.error = null;
      this.movie = null;
      this.showTrailerModal = false;
      this.fetchMovieData();
      document.title = 'THE MOVIE DB';
      window.scrollTo({ top: 0, behavior: 'smooth' });
      this.showSuccessMessage('🏠 Returned to home page.');
    },

    addToList() {
              this.isInList = !this.isInList;
    },

    toggleLike() {
              this.isLiked = !this.isLiked;
    },

    toggleBookmark() {
              this.isBookmarked = !this.isBookmarked;
    },

    toggleRating() {
              if (this.userRating > 0) {
          this.userRating = 0;
        } else {
          this.userRating = 7;
        }
    },

    showRatingModal() {
      this.showRatingModal = true;
    },

    submitRating() {
      this.showRatingModal = false;
    },

    login() {
      if (this.loginForm.username && this.loginForm.password) {
        if (this.loginForm.username === 'demo' && this.loginForm.password === 'password') {
          this.isLoggedIn = true;
          this.currentUser = { username: this.loginForm.username };
          this.showLoginModal = false;
          this.loginForm = { username: '', password: '' };
          alert('Welcome back to TMDB!');
          return;
        }
        
        if (this.createdUsers) {
          const user = this.createdUsers.find(u => 
            u.username === this.loginForm.username && u.password === this.loginForm.password
          );
          
          if (user) {
            this.isLoggedIn = true;
            this.currentUser = { username: this.loginForm.username };
            this.showLoginModal = false;
            this.loginForm = { username: '', password: '' };
            alert(`Welcome back, ${this.loginForm.username}!`);
            return;
          }
        }
        
        alert('Invalid username or password. Try demo/password or use your created account.');
      } else {
        alert('Please fill in all fields');
      }
    },

    signup() {
      if (this.signupForm.username && this.signupForm.email && this.signupForm.password) {
        this.createdUsers = this.createdUsers || [];
        this.createdUsers.push({
          username: this.signupForm.username,
          email: this.signupForm.email,
          password: this.signupForm.password
        });
        
        this.showSignupModal = false;
        this.signupForm = { username: '', email: '', password: '' };
        alert('Account created successfully! You can now login with your credentials.');
      } else {
        alert('Please fill in all fields');
      }
    },

    logout() {
      alert('Logged out!');
      this.isLoggedIn = false;
      this.currentUser = { username: 'Guest' };
    },

    submitReview() {
      if (this.newReview.author && this.newReview.rating && this.newReview.text) {
        const review = {
          id: Date.now(),
          author: this.newReview.author,
          rating: parseInt(this.newReview.rating),
          text: this.newReview.text,
          date: new Date().toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })
        };
        
        // Add to current reviews if we're viewing a specific movie, otherwise add to general reviews
        if (this.currentReviews.length > 0) {
          this.currentReviews.unshift(review);
        } else {
          this.reviews.unshift(review);
        }
        
        // Reset form
        this.newReview = { author: '', rating: '', text: '' };
        
        this.showSuccessMessage('✅ Review submitted successfully!');
      } else {
        alert('Please fill in all fields');
      }
    },

    submitDiscussion() {
      if (this.newDiscussion.author && this.newDiscussion.title && this.newDiscussion.preview) {
        const discussion = {
          id: Date.now(),
          title: this.newDiscussion.title,
          author: this.newDiscussion.author,
          preview: this.newDiscussion.preview,
          date: new Date().toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          }),
          replies: 0
        };
        
        // Add to current discussions if we're viewing a specific movie, otherwise add to general discussions
        if (this.currentDiscussions.length > 0) {
          this.currentDiscussions.unshift(discussion);
        } else {
          this.discussions.unshift(discussion);
        }
        
        // Reset form
        this.newDiscussion = { author: '', title: '', preview: '' };
        
        this.showSuccessMessage('💬 Discussion started successfully!');
      } else {
        alert('Please fill in all fields');
      }
    }
  }
}
</script>

<style scoped>
/* Hero Section Styles */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  z-index: 1;
}

.hero-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(0, 0, 0, 0.6) 50%,
    rgba(0, 0, 0, 0.8) 100%
  );
  z-index: 2;
}

.hero-content {
  position: relative;
  z-index: 3;
  width: 100%;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.enhanced-features {
  background-color: #0f1419;
  padding: 2rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background-color: #1a1d29;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h4 {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.feature-card p {
  color: #cccccc;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.device-icons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 2rem;
}

.overview-section {
  margin-top: 2rem;
}

.overview-section h3 {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.poster-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.movie-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.movie-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.back-home-btn {
  background: linear-gradient(135deg, #00d4ff, #00b8e6);
  color: #000;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.back-home-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
}

.tagline {
  font-style: italic;
  color: #cccccc;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

/* Cast & Crew Section */
.cast-crew {
  background-color: #1a1d29;
  padding: 3rem 0;
}

.cast-crew h3 {
  color: #ffffff;
  font-size: 1.8rem;
  margin-bottom: 2rem;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.cast-item {
  background-color: #0f1419;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.cast-item:hover {
  transform: translateY(-5px);
}

.cast-photo {
  height: 200px;
  overflow: hidden;
}

.cast-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cast-info {
  padding: 1rem;
}

.cast-name {
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.cast-role {
  color: #cccccc;
  font-size: 0.9rem;
}

.view-more-btn {
  background: transparent;
  border: 1px solid #00d4ff;
  color: #00d4ff;
  padding: 0.8rem 2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.view-more-btn:hover {
  background-color: #00d4ff;
  color: #000;
}

/* Social Section */
.social-section {
  background-color: #0f1419;
  padding: 3rem 0;
}

.social-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tab-btn {
  background: transparent;
  border: none;
  color: #cccccc;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.3s ease;
}

.tab-btn.active {
  color: #00d4ff;
  border-bottom: 2px solid #00d4ff;
}

.reviews-content, .discussions-content {
  background-color: #1a1d29;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.review-item, .discussion-item {
  padding: 1rem 0;
  border-bottom: 1px solid #333;
}

.review-item:last-child, .discussion-item:last-child {
  border-bottom: none;
}

.review-header, .discussion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.reviewer-name, .discussion-title {
  font-weight: bold;
  color: #ffffff;
}

.review-date, .discussion-meta {
  color: #888;
  font-size: 0.9rem;
}

.review-rating {
  background-color: #00d4ff;
  color: #000;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-weight: bold;
}

.review-text, .discussion-preview {
  color: #cccccc;
  line-height: 1.6;
  margin-top: 0.5rem;
}

.discussion-meta span {
  margin-right: 1rem;
}

/* Review and Discussion Form Styles */
.add-review-form, .add-discussion-form {
  background-color: #2a2f3b;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #333;
}

.add-review-form h4, .add-discussion-form h4 {
  color: #00d4ff;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: #cccccc;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: bold;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  background: #1a1d29;
  border: 1px solid #333;
  border-radius: 6px;
  color: #ffffff;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.reviews-list, .discussions-list {
  margin-top: 2rem;
}

.reviews-list h4, .discussions-list h4 {
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
}

/* User Menu Styles */
.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: #00d4ff;
  font-weight: bold;
}

/* Action Buttons Styles */
.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.action-btn {
  background: transparent;
  border: 1px solid #333;
  color: #cccccc;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn:hover {
  background-color: #00d4ff;
  color: #000;
  border-color: #00d4ff;
}

.action-btn.play-trailer {
  background: linear-gradient(135deg, #00d4ff, #00b8e6);
  color: #000;
  border-color: #00d4ff;
}

.action-btn.play-trailer:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
}

/* Media Section */
.media-section {
  background-color: #1a1d29;
  padding: 3rem 0;
}

.media-section h3 {
  color: #ffffff;
  font-size: 1.8rem;
  margin-bottom: 2rem;
}

.media-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.media-tab {
  background: transparent;
  border: none;
  color: #cccccc;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  font-weight: bold;
  transition: color 0.3s ease;
}

.media-tab.active {
  color: #00d4ff;
  border-bottom: 2px solid #00d4ff;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.media-item {
  aspect-ratio: 2/3;
  overflow: hidden;
  border-radius: 8px;
}

.media-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.media-item:hover img {
  transform: scale(1.1);
}

/* IMPROVEMENT 1: Smart Recommendations Styles */
.smart-recommendations {
  background-color: #0f1419;
  padding: 3rem 0;
}

.recommendations-header {
  text-align: center;
  margin-bottom: 2rem;
}

.recommendations-header h3 {
  color: #00d4ff;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.recommendations-header p {
  color: #cccccc;
  font-size: 1.1rem;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.recommendation-card {
  background-color: #1a1d29;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.recommendation-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.rec-poster {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.rec-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recommendation-card:hover .rec-poster img {
  transform: scale(1.1);
}

.rec-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.recommendation-card:hover .rec-overlay {
  opacity: 1;
}

.rec-info {
  padding: 1.5rem;
}

.rec-info h4 {
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.rec-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.rec-year {
  color: #cccccc;
}

.rec-rating {
  color: #00d4ff;
  font-weight: bold;
}

.rec-reason {
  color: #cccccc;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.rec-match {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.match-bar {
  flex: 1;
  height: 6px;
  background-color: #333;
  border-radius: 3px;
  overflow: hidden;
}

.match-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #00b8e6);
  transition: width 0.3s ease;
}

.rec-match span {
  color: #00d4ff;
  font-size: 0.9rem;
  font-weight: bold;
}

/* IMPROVEMENT 2: Trailer Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.trailer-modal {
  background: #1a1d29;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #333;
}

.modal-header h3 {
  color: #ffffff;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #333;
}

.trailer-container {
  padding: 2rem;
}

.trailer-placeholder {
  background: linear-gradient(135deg, #0f1419, #1a1d29);
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  border: 2px dashed #333;
}

.trailer-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.control-btn {
  background-color: #00d4ff;
  color: #000;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.control-btn:hover {
  background-color: #00b8e6;
  transform: translateY(-2px);
}

.trailer-info {
  color: #cccccc;
}

.trailer-info p {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.trailer-stats {
  display: flex;
  gap: 2rem;
  justify-content: center;
  font-size: 0.9rem;
  color: #888;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem 2rem;
  border-top: 1px solid #333;
}

/* Auth Modal Styles */
.auth-modal {
  background: #1a1d29;
  border-radius: 12px;
  max-width: 400px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.auth-content {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: #cccccc;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: #2a2f3b;
  border: 1px solid #333;
  border-radius: 6px;
  color: #ffffff;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #00d4ff;
}

/* Rating Modal Styles */
.rating-modal {
  background: #1a1d29;
  border-radius: 12px;
  max-width: 400px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.rating-content {
  padding: 2rem;
  text-align: center;
}

.stars {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.star {
  font-size: 2.5rem;
  color: #333;
  cursor: pointer;
  transition: color 0.3s ease;
}

.star:hover {
  color: #00d4ff;
}

.star.active {
  color: #00d4ff;
}

.rating-text {
  font-size: 2rem;
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 1.5rem;
}

/* Navigation Notification Styles */
.navigation-notification {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.9);
  color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  z-index: 2000;
  animation: fadeInUp 0.3s ease;
}

.notification-content {
  text-align: center;
}

.notification-content span {
  display: block;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: bold;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: #00d4ff;
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate(-50%, -30%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

@keyframes pulse {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* Success Notification Styles */
.success-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, #00d4ff, #00b8e6);
  color: #000;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  z-index: 2000;
  animation: slideInRight 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
}

.success-content span {
  font-weight: bold;
  font-size: 1rem;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 768px) {
  .recommendations-grid {
    grid-template-columns: 1fr;
  }
  
  .trailer-modal {
    margin: 1rem;
    max-height: 95vh;
  }
  
  .trailer-controls {
    flex-direction: column;
  }
  
  .trailer-stats {
    flex-direction: column;
    gap: 0.5rem;
  }

  .movie-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .back-home-btn {
    align-self: flex-start;
  }

  .cast-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }

  .media-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
}
</style> 