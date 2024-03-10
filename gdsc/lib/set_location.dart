import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'main.dart' as mc;

final LatLng? selectedLocation = mc.currentPosition;


class SetLocation extends StatefulWidget{
  const SetLocation({super.key});

  @override 
  State createState() => _SetLocationState();
  
}

class _SetLocationState extends State<SetLocation>{
  void _setLocation(LatLng location) {
    setState(() {
      mc.currentPosition = location;
      //print("location_set: $location");
      mc.mode = 1;
      Navigator.push(context, MaterialPageRoute(builder: (context) => const mc.MyApp()));
    });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Location'),
      ),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: selectedLocation ?? const LatLng(22.632820, 120.300487),
              zoom: 11.0,
            ),
            onTap: _setLocation,
          ),
        ],
      ),
    );
  }
}