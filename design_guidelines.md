# Design Guidelines - Sanad Medical AI Website

## Design Approach

**Reference-Based + Custom Specification**: This medical application has explicit design requirements combining modern glassmorphism aesthetics with Arabic-first UX patterns. The design follows the detailed specifications provided while maintaining medical application best practices.

---

## Core Visual Identity

### Color System
- **Primary Background**: Linear gradient from Deep Blue (#1e3c72) to Purple (#2a5298) - fixed attachment for depth
- **Glass Containers**: Translucent white backgrounds `rgba(255, 255, 255, 0.7)` with `backdrop-filter: blur(10px)`
- **Text Colors**: Dark Grey/Blue for optimal readability on glass surfaces
- **Interactive Elements**: Gradient from #667eea to #764ba2 for buttons and accents
- **Semantic Colors**:
  - Success/Positive: Green gradient (#84fab0 to #8fd3f4)
  - Warning: Orange gradient (#f6d365 to #fda085)
  - Info: Blue gradient (#a1c4fd to #c2e9fb)
  - Danger/Negative: Red gradient (#ff6b6b to #ee5a6f)

### Typography
- **Primary Fonts**: Tajawal and Cairo from Google Fonts
- **Weights**: 300, 400, 500, 700, 900
- **Direction**: RTL (Right-to-Left) enforced globally
- **Hierarchy**:
  - H1: 3em, weight 900, centered, gradient text effect
  - H2/H3: weight 700, centered, #2d3748
  - Body: 16-18px, weight 400
  - Buttons: 18px, weight 700

---

## Layout System

### Spacing
- **Glass Cards**: 30px padding, 20px margin vertical
- **Form Inputs**: 15px padding
- **Buttons**: 15px vertical, 30px horizontal
- **Sections**: 20px spacing between major elements

### Glass Container Properties
- Border radius: 20px
- Box shadow: `0 8px 32px rgba(0, 0, 0, 0.1)`
- Border: `1px solid rgba(255, 255, 255, 0.2)`
- Hover lift: `-5px translateY` with enhanced shadow

---

## Page-Specific Components

### 1. Landing/Home Page
**Hero Section**:
- Full viewport height with gradient background
- Centered large heading with gradient text effect
- Three feature cards in responsive grid (1 column mobile, 3 desktop)

**Feature Cards**:
- Glass background with gradient overlay
- Large emoji/icon (48px)
- Bold title
- Descriptive text in gray (#718096)
- Hover: Scale 1.05 + translateY(-10px) + border color #667eea
- Shadow enhancement on hover

### 2. Farah (Mental Health) Page
**Layout**:
- Glass card container
- RTL textarea for Arabic input
- Gradient submit button
- Result box with conditional styling

**Result Display**:
- Animated slide-in appearance (0.5s ease)
- Color-coded based on sentiment (green/yellow/red gradients)
- Large emoji indicator
- Confidence percentage display
- Personalized advice text

### 3. Smart Doctor Chatbot Page
**Chat Interface**:
- Modern messaging app aesthetic
- Chat bubbles with glass effect
- User messages: Aligned right (RTL)
- AI messages: Aligned left
- Message counter display
- Quick question buttons below chat input

**Input Area**:
- Glass textarea with RTL
- Gradient send button
- Quick action buttons with glass background

### 4. Emotion Mirror Page
**Layout**:
- Three-column metric dashboard (stacks on mobile)
- Image upload area with glass styling
- Results in metric cards

**Metric Cards**:
- Glass background
- Large value display (2em, #667eea)
- Label text
- Emoji indicators
- Progress/score visualizations

---

## Interactive Elements

### Buttons
- **Primary**: Gradient background (#667eea to #764ba2)
- Border radius: 15px
- Box shadow: `0 4px 15px rgba(102, 126, 234, 0.4)`
- Hover: TranslateY(-2px) + enhanced shadow
- No active/focus states needed - gradient handles all contexts

### Form Inputs
- Border radius: 15px
- Border: 2px solid #e2e8f0
- RTL text alignment
- Focus: Border color #667eea with subtle glow
- Transition: All 0.3s ease

### Animations
- **Result boxes**: Slide-in from bottom (opacity 0→1, translateY 20px→0)
- **Cards**: Hover scale and lift effect
- **Buttons**: Subtle scale on hover
- **Transitions**: 0.3-0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) for bouncy feel

---

## Navigation

**Sidebar (if multi-page)**:
- Dark gradient background (#2d3748 to #1a202c)
- White text throughout
- Glass effect on hover states

**Top Navigation (if SPA)**:
- Glass navbar with blur
- RTL menu items
- Active state with gradient underline

---

## Accessibility & RTL

- All text inputs: `direction: rtl, text-align: right`
- All containers: RTL flow
- Form labels: Right-aligned
- Icons: Flipped where directional (arrows, etc.)
- Focus indicators: Visible and high contrast

---

## Images

**No large hero images specified** - This application relies on gradient backgrounds and glassmorphism for visual impact. Icon/emoji usage is preferred for representing features and emotions.

---

## Special Considerations

**Medical Context**:
- Clear warning messages about not replacing professional medical advice
- Emergency contact information easily accessible
- Privacy notices about data handling
- Professional, trustworthy aesthetic balanced with approachability

**Arabic-First Design**:
- All text flows RTL naturally
- Numbers and technical terms maintain readability
- Icon meanings clear across cultures
- Emojis used universally (medical symbols, emotions)

**Performance**:
- Backdrop-filter graceful degradation
- Smooth animations without janky performance
- Optimized for mobile devices
- Fast initial load despite glassmorphism effects