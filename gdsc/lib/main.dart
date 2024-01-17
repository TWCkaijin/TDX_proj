import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    name: "potent-result-406711",
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State createState() => _MyAppState();

  // This widget is the root of your application.
}

class _MyAppState extends State {
  late GoogleMapController mapController;

  final LatLng _center = const LatLng(22.6239974, 120.2981408);

  void _onMapCreated(GoogleMapController controller) {
    mapController = controller;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        home: Scaffold(
          extendBodyBehindAppBar: true,
          appBar: AppBar(
            backgroundColor: Colors.transparent,
            elevation: 0,
            centerTitle: true,
            title: Container(
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: Colors.blue[100],
                borderRadius: BorderRadius.circular(15.0),
              ),
              child: Text(
                'App Name',
                style: TextStyle(color: Colors.grey[800], fontSize: 20),
              ),
            ),
          ),
          body: Stack(
            children: <Widget>[
              GoogleMap(
                onMapCreated: _onMapCreated,
                initialCameraPosition: CameraPosition(
                  target: _center,
                  zoom: 12.5,
                ),
                myLocationButtonEnabled: false,
                zoomControlsEnabled: false,
              ),
              DraggableScrollableSheet(
                initialChildSize: 0.3,
                minChildSize: 0.05,
                maxChildSize: 0.9,
                builder:
                    (BuildContext context, ScrollController scrollController) {
                  return Container(
                    decoration: BoxDecoration(
                      color: Colors.blue[100],
                      // remove or decrease the borderRadius
                      borderRadius: const BorderRadius.vertical(
                          top: Radius.circular(20.0)),
                    ),
                    child: ListView.builder(
                      controller: scrollController,
                      itemCount: 25,
                      itemBuilder: (BuildContext context, int index) {
                        return ListTile(title: Text('Item $index'));
                      },
                      padding: EdgeInsets.zero,
                    ),
                  );
                },
              ),
            ],
          ),
        ));
  }
}
