import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

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
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final MaterialStateProperty<Icon?> thumbIcon =
      MaterialStateProperty.resolveWith<Icon?>(
    (Set<MaterialState> states) {
      if (states.contains(MaterialState.selected)) {
        return const Icon(Icons.lightbulb_outline);
      }
      return const Icon(Icons.lightbulb);
    },
  );
  final MaterialStateProperty<Color?> thumbColor =
      MaterialStateProperty.resolveWith<Color?>(
    (Set<MaterialState> states) {
      if (states.contains(MaterialState.selected)) {
        return Colors
            .transparent; // Change this to your desired color for dark mode
      }
      return null; // Change this to your desired color for light mode
    },
  );
  final MaterialStateProperty<Color?> trackColor =
      MaterialStateProperty.resolveWith<Color?>(
    (Set<MaterialState> states) {
      // Track color when the switch is selected.
      if (states.contains(MaterialState.selected)) {
        return Colors.blueGrey[600];
      }
      return null;
    },
  );

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
                
Email and Github is provided below.''',
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
                'empty',
              ),
            ),
            Container(
              padding: const EdgeInsets.all(10.0),
              margin:
                  const EdgeInsets.symmetric(horizontal: 25.0, vertical: 10.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.black, width: 2.0),
              ),
              child: const Text(
                'empty',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
