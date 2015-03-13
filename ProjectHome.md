The **WLCP** (We Love ChinesePod) software aims to make learning Chinese from the [ChinesePod](http://www.chinesepod.com/) website much more effective and efficient by allowing [premium content subscribers](http://chinesepod.com/help/subscription) to easily download lessons for off-line/mobile usage in a user-customizable format.

**WLCP** is implemented as a [Python](http://www.python.org/) script that downloads ChinesePod lesson data and stores it in [XML](http://www.w3.org/TR/REC-xml/) and [MP3](http://www.iis.fraunhofer.de/EN/bf/amm/projects/mp3/) format; [XSLT](http://www.w3.org/TR/xslt) and [CSS](http://www.w3.org/TR/CSS21/) stylesheets then allow for transparent, user-customizable rendering of the lessons.

## News ##
  * **September 12, 2009** Version 2009.09.12 has been released ([view changes](Changes.md))
  * **June 28, 2009** Version 2009.06.26 has been released ([view changes](Changes.md))
  * **March 26, 2009** Derek Chadwick has created [SeePod Lesson Manager](http://www.seepod.net/); it includes a GUI for WLCP, making it easier to use!
  * **March 22, 2009** Version 2009.03.22 released ([view changes](Changes.md)) ([view forum post](http://chinesepod.com/community/conversations/post/4628))
  * **February 16, 2009** [WLCP broke with the ChinesePod site upgrade](http://chinesepod.com/community/conversations/post/4444); a new parser will eventually come
  * **February 9, 2009** Version 2009.02.09 released ([view changes](Changes.md)) ([view screenshot](http://wlcp.googlecode.com/files/wlcpod-1-screenshot.png)) ([view forum post](http://chinesepod.com/community/conversations/post/4356))

## Features ##
To help users learn _on their terms_, WLCP automatically downloads, for a specified lesson, the following **user-customizable content** (or any user-specified portion of it):
  1. An XML file, **viewable in [Firefox](http://www.mozilla.com/firefox/)**, which displays the lesson in a user-customizable format involving any combination of the following via user-configurable (through CSS and XSLT) fonts, colours and sizes.  For instance, the provided default XSLT and CSS stylesheets feature extremely easy to use toggle buttons used to
    * switch between **traditional** and **simplified** Chinese characters
    * show or hide the original **Chinese text**
    * show or hide the **English semantic translations**
    * show or hide the **pinyin sentence translations**
    * switch between **highly readable tooltips** and **character annotations** to provide extra character information
    * make the study page suitable for **printing**
> > The tooltips contain **hyperlinks** to the following freely available online resources:
    * [Taiwanese Ministry of Education](http://www.moe.gov.tw/)'s [Learning Program for Stroke Order of Frequently Used Chinese Characters](http://stroke-order.learningweb.moe.edu.tw/)
    * [Chinese University of Hong Kong](http://humanum.arts.cuhk.edu.hk/)'s [Chinese Character Database: With Word-formations Phonologically Disambiguated According to the Cantonese Dialect](http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/)
    * [Adam Sheik](http://www.cantonese.sheik.co.uk/)'s [CantoDict Project: A Collaborative English/Cantonese/Mandarin Dictionary](http://www.cantodict.org/)
> > The character annotations provide **literal** ("word-for-word") translations in English, as well as pronunciation symbols in **pinyin** or **bopomofo** format.
  1. **MP3 files** incorporated into the XML-generated webpage; WLCP downloads any combination of:
    * lesson, dialogue and audio review MP3s
    * expansion and dialogue sentences, and key and supplementary vocabulary; these files are assembled into larger files to facilitate their transfer to other devices, such as portable MP3 players
  1. traditional and/or simplified HTML and PDF **lesson transcripts**; a [LaTeX](http://www.latex-project.org/) stylesheet is provided to generate user-customizable PDFs
  1. bonus: WLCP also generates pretty **lists of downloaded lessons**. By default, these are:
    * lessons/wlcpod-index.xml: lessons downloaded during the last WLCP session
    * lessons/wlcpod-master-index.xml: all lessons downloaded to date


> After bookmarking these two pages in Firefox, one can then use them as starting pages when searching for WLCP'ed lessons instead of manually locating files -- the lesson pictures and description should aid recognition of previously studied lessons.

Additional functions supported by WLCP:
  1. [PlecoDict](http://www.pleco.com/) Export
  1. character annotation (via the Firefox [Ruby](https://addons.mozilla.org/en-US/firefox/addon/1935) plugin), whereby each character is directly annotated with the corresponding pinyin (instead of each on separate lines); this features
    * selective hiding of pinyin/bopomofo for user-specified characters
    * literal translations of the sentences (你好 = "you good", 你在哪兒 = "you located where")

## Basic Usage ##
### Installation ###
  1. Install Python if necessary.
    * Windows users: Download and install [Python for Windows](http://www.python.org/ftp/python/2.6.1/python-2.6.1.msi).
    * Mac users: Python is already installed.
    * Ubuntu users: Python is already installed.
  1. [Download WLCP](http://code.google.com/p/wlcp/downloads) and unzip the downloaded file.
  1. For best results, install the **AR PL ZenKai Uni** and **AR PL ShanHeiSun Uni** fonts, either by enabling Chinese support in your operating system or as below.
    * Windows users: search for this font online and download it; one possible location is [here](http://www.cantonese.sheik.co.uk/fonts.htm).
    * Mac users: the substitute font **BiauKai** may already be installed
    * RedHat users: `yum search fonts-chinese`
    * Ubuntu users: `aptitude search language-support-fonts-zh`
    * Debian users: http://tavi.debian.org.tw/index.php?page=Unifonts

### Downloading a lesson with WLCP ###
  1. Run the script.
    * Windows users: Double-click on `wlcpod.py`.
    * Mac users: Click on `wlcpod.py`, then click on "Run" at the top of the program, then click on "Run Module".
    * Ubuntu users: Double-click on `wlcpod.py`, and click on "Run in terminal".
  1. Follow the instructions in the black box that pops up. It will ask for your e-mail address, password, and the name of the lesson (exactly as it appears in the URL) that you want to download. This information is sent only to the Praxis log-in site -- you may verify this for yourself by looking at the source code. Once supplied with the lesson name, WLCP will then download the necessary content from ChinesePod.

#### Example ####
To download the lesson called "going-to-the-gym", the lesson name must be entered exactly as that.
  * Right: `going-to-the-gym`
  * Wrong: `Going to the gym`
  * Wrong: `Goingtothegym`
For this lesson, WLCP would download or create the following files:
  * `lessons/wlcpod-master-index.xml` (Master index XML file --- **view this file in Firefox** to see a conveniently accessible list of all WLCP-downloaded lessons to date)
  * `lessons/wlcpod-index.xml` (Last WLCP session index XML file)
  * `lessons/going-to-the-gym.xml` (Lesson XML file -- **view this file in Firefox** to study the WLCP-enhanced lesson)
  * `lessons/going-to-the-gym/going-to-the-gym_dialogue.mp3` (Lesson dialogue MP3)
  * `lessons/going-to-the-gym/going-to-the-gym_lesson.mp3` (Lesson full podcast MP3)
  * `lessons/going-to-the-gym/going-to-the-gym_review.mp3` (Lesson audio review MP3)
  * `lessons/going-to-the-gym/going-to-the-gym_dialogue_sentences.mp3` (All dialogue tab readings in one MP3)
  * `lessons/going-to-the-gym/going-to-the-gym_expansion_sentences.mp3` (All expansion tab readings in one MP3)
  * `lessons/going-to-the-gym/going-to-the-gym_vocabulary_sentences.mp3` (All vocabulary tab readings in one MP3)
  * `lessons/going-to-the-gym/going-to-the-gym.jpeg` (Lesson picture)
  * `lessons/going-to-the-gym/going-to-the-gym-simp.pdf` (Simplified character PDF transcript)
  * `lessons/going-to-the-gym/going-to-the-gym-trad.pdf` (Traditional character PDF transcript)
  * `lessons/going-to-the-gym/going-to-the-gym-simp.html` (Simplified character HTML transcript)
  * `lessons/going-to-the-gym/going-to-the-gym-trad.html` (Traditional character HTML transcript)

## Advanced usage ##

### Configuring WLCP ###
In the same folder as `wlcpod.py` is a configuration file called `wlcpod.ini`. You can edit it to configure WLCP with your desired settings, such as:
  * your login information (e-mail and password) -- this spares you from having to enter your log-in information with each WLCP invocation
  * which files WLCP actually downloads
  * other more advanced options
To edit the `wlcpod.ini` file, any text editor on Linux or Mac OS should work; on Windows, Notepad does not work due to incorrect handling of linefeeds, so use an editor such as WordPad instead.

### Downloading multiple lessons ###
If you'd like to download multiple lessons at once (or download a lesson with Chinese characters in its name), create a file called `lessons.txt` ([example](http://cds.gmu.edu/~acorriga/chinese/lessons.txt)) which contains the names of the desired lessons, exactly as they appear in the URLs, listed one per line.

## Acknowledgement ##

For playing the recorded Chinese audio, WLCP uses the excellent [neolao Flash MP3 Player](http://flash-mp3-player.net/players/maxi/).

## Contact information ##

WLCP was developed by [Andrew Corrigan](http://cds.gmu.edu/~acorriga/) and [Jonathan Lee](http://math.stanford.edu/~jlee/).

## Disclaimer ##
This software does _NOT_ provide access to or distribute premium content to people who do not already have access to it. This software merely automates, for an _INDIVIDUAL PREMIUM SUBSCRIBER,_ the process of downloading and displaying material provided by ChinesePod.
For example, many users already manually [copy-and-paste the expansion sentences into a document and print this out](http://chinesepod.com/community/conversations/post/2058), or [manually create a practice MP3 file of the expansion sentences for their own personal use](http://chinesepod.com/community/conversations/post/2137). This is exactly what this program does, it only automates the process. It is intended for those of us who want to practice the expansion sentences "on our terms" away from the computer. This makes ChinesePod a more [mobile form of learning](http://chinesepod.com/community/conversations/post/2331).