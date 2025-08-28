import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

class ThemeModel extends ChangeNotifier {
  bool _isDarkMode = false;
  bool _mapStyleChanged = false;

  bool get isDarkMode => _isDarkMode;
  bool get mapStyleChanged => _mapStyleChanged;

  set mapStyleChanged(bool value) {
    _mapStyleChanged = value;
    notifyListeners();
  }

  void toggleTheme() {
    _isDarkMode = !_isDarkMode;
    _mapStyleChanged = true;
    notifyListeners();
  }
}

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  SettingsPageState createState() => SettingsPageState();
}

class SettingsPageState extends State<SettingsPage> {
  final WidgetStateProperty<Icon?> thumbIcon =
      WidgetStateProperty.resolveWith<Icon?>(
    (Set<WidgetState> states) {
      if (states.contains(WidgetState.selected)) {
        return const Icon(Icons.lightbulb_outline);
      }
      return const Icon(Icons.lightbulb);
    },
  );
  final WidgetStateProperty<Color?> thumbColor =
      WidgetStateProperty.resolveWith<Color?>(
    (Set<WidgetState> states) {
      if (states.contains(WidgetState.selected)) {
        return Colors
            .transparent; // Change this to your desired color for dark mode
      }
      return null; // Change this to your desired color for light mode
    },
  );
  final WidgetStateProperty<Color?> trackColor =
      WidgetStateProperty.resolveWith<Color?>(
    (Set<WidgetState> states) {
      // Track color when the switch is selected.
      if (states.contains(WidgetState.selected)) {
        return Colors.blueGrey[600];
      }
      return null;
    },
  );

  @override
  Widget build(BuildContext context) {
    final themeModel = Provider.of<ThemeModel>(context);
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(50.0),
        child: SafeArea(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 25.0),
            decoration: BoxDecoration(
              color: themeModel.isDarkMode
                  ? Colors.blueGrey[800]
                  : Colors.blueGrey[100],
              borderRadius: BorderRadius.circular(30.0),
            ),
            child: AppBar(
              backgroundColor: Colors.transparent,
              elevation: 0,
              centerTitle: true,
              title: const Text(
                'Settings',
                style: TextStyle(
                  fontSize: 20.0,
                  fontWeight: FontWeight.w400,
                  letterSpacing: 3.0,
                ),
              ),
            ),
          ),
        ),
      ),
      body: Center(
        child: Switch(
          thumbColor: thumbColor,
          thumbIcon: thumbIcon,
          trackColor: trackColor,
          value: themeModel.isDarkMode,
          onChanged: (value) {
            setState(() {
              themeModel.toggleTheme();
            });
          },
        ),
      ),
    );
  }
}

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    final themeModel = Provider.of<ThemeModel>(context);
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(50.0),
        child: SafeArea(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 25.0),
            decoration: BoxDecoration(
              color: themeModel.isDarkMode
                  ? Colors.blueGrey[800]
                  : Colors.blueGrey[100],
              borderRadius: BorderRadius.circular(30.0),
            ),
            child: AppBar(
              backgroundColor: Colors.transparent,
              elevation: 0,
              centerTitle: true,
              title: const Text(
                'About',
                style: TextStyle(
                  fontSize: 20.0,
                  fontWeight: FontWeight.w400,
                  letterSpacing: 3.0,
                ),
              ),
            ),
          ),
        ),
      ),
      body: Align(
        alignment: Alignment.topCenter,
        child: Column(
          children: <Widget>[
            Container(
              padding: const EdgeInsets.all(10.0),
              margin:
                  const EdgeInsets.symmetric(horizontal: 25.0, vertical: 10.0),
              child: const Text(
                '''Hi! Welcome to the app, it is a simple map app made by simple people. Enjoy!
                
Also, feel free to contact us with any feedback or suggestions.
                
Github is provided below.''',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 15.0,
                  fontWeight: FontWeight.w300,
                  letterSpacing: 1.0,
                ),
              ),
            ),
            InkWell(
              onTap: () async {
                Uri url = Uri.parse('https://github.com/TWCkaijin/TDX_proj');
                if (await canLaunchUrl(url)) {
                  await launchUrl(url);
                } else {
                  throw 'Could not launch $url';
                }
              },
              child: Container(
                padding: const EdgeInsets.all(10.0),
                margin: const EdgeInsets.symmetric(
                    horizontal: 25.0, vertical: 10.0),
                child: const Text(
                  'Go to our Github',
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}

class BugPage extends StatelessWidget {
  const BugPage({super.key});

  @override
  Widget build(BuildContext context) {
    final themeModel = Provider.of<ThemeModel>(context);
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(50.0),
        child: SafeArea(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 25.0),
            decoration: BoxDecoration(
              color: themeModel.isDarkMode
                  ? Colors.blueGrey[800]
                  : Colors.blueGrey[100],
              borderRadius: BorderRadius.circular(30.0),
            ),
            child: AppBar(
              backgroundColor: Colors.transparent,
              elevation: 0,
              centerTitle: true,
              title: const Text(
                'Bug Report',
                style: TextStyle(
                  fontSize: 20.0,
                  fontWeight: FontWeight.w400,
                  letterSpacing: 3.0,
                ),
              ),
            ),
          ),
        ),
      ),
      body: Align(
        alignment: Alignment.topCenter,
        child: Column(
          children: <Widget>[
            Container(
              padding: const EdgeInsets.all(10.0),
              margin:
                  const EdgeInsets.symmetric(horizontal: 25.0, vertical: 10.0),
              child: const Text(
                '''Sorry that we messed up
Please provide us with the following information:''',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 15.0,
                  fontWeight: FontWeight.w300,
                  letterSpacing: 1.0,
                ),
              ),
            ),
            Container(
              padding: const EdgeInsets.all(10.0),
              margin:
                  const EdgeInsets.symmetric(horizontal: 25.0, vertical: 10.0),
              child: const Text(
                '''-What happened?
-What were you doing?
-What device were you using?

Also a screenshot would be helpful''',
                textAlign: TextAlign.left,
                style: TextStyle(
                  fontSize: 15.0,
                  fontWeight: FontWeight.w300,
                  letterSpacing: 1.0,
                ),
              ),
            ),
            InkWell(
              onTap: () async {
                Uri url =
                    Uri.parse('https://github.com/TWCkaijin/TDX_proj/issues');
                if (await canLaunchUrl(url)) {
                  await launchUrl(url);
                } else {
                  throw 'Could not launch $url';
                }
              },
              child: Container(
                padding: const EdgeInsets.all(10.0),
                margin: const EdgeInsets.symmetric(
                    horizontal: 25.0, vertical: 10.0),
                child: const Text(
                  'Report Bug',
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
