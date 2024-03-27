import UIKit
import Flutter
import GoogleMaps

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    GeneratedPluginRegistrant.register(with: self)
    if let path = Bundle.main.path(forResource: "Keys", ofType: "plist"),
       let dict = NSDictionary(contentsOfFile: path) as? [String: AnyObject],
       let apiKey = dict["googleMapsApiKey"] as? String {
      GMSServices.provideAPIKey(apiKey)
    } else {
      fatalError("Failed to load Google Maps API key")
    }
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}