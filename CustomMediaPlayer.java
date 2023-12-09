import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.geometry.Pos;
import javafx.scene.layout.HBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.stage.Stage;
import javafx.util.Duration;

public class CustomMediaPlayer extends Application {

    private static String mediaPath;
    private static int frameNumber;

    @Override
    public void start(Stage primaryStage) {
        // Load the media file from the provided path
        Media media = new Media(mediaPath);
        MediaPlayer mediaPlayer = new MediaPlayer(media);
        MediaView mediaView = new MediaView(mediaPlayer);

        // Setup the media player
        mediaPlayer.setOnReady(() -> {
            if (frameNumber > 0) {
                double frameRate = 30.0;
                double timeInSeconds = frameNumber / frameRate;
                mediaPlayer.seek(Duration.seconds(timeInSeconds));
            }
        });

        // Play button
        Button playButton = new Button("Play");
        playButton.setOnAction(e -> {
            mediaPlayer.play();
            if (frameNumber > 0) {
                double frameRate = 30.0;
                double timeInSeconds = frameNumber / frameRate;
                mediaPlayer.seek(Duration.seconds(timeInSeconds));
            }
        });

        // Pause button
        Button pauseButton = new Button("Pause");
        pauseButton.setOnAction(e -> mediaPlayer.pause());

        // Reset button
        Button resetButton = new Button("Reset");
        resetButton.setOnAction(e -> {
            mediaPlayer.play();
            mediaPlayer.seek(Duration.seconds(0));
        });

        // Layout for buttons
        HBox controlBox = new HBox(playButton, pauseButton, resetButton);
        controlBox.setSpacing(10);
        controlBox.setAlignment(Pos.BOTTOM_CENTER);

        // Overlay the mediaView and controlBox using a StackPane
        StackPane stackPane = new StackPane();
        stackPane.getChildren().addAll(mediaView, controlBox);
        StackPane.setAlignment(controlBox, Pos.BOTTOM_CENTER); // Position the controlBox at the bottom left

        Scene scene = new Scene(stackPane, 352, 288);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        // Check if arguments are provided
        if (args.length < 2) {
            System.exit(1);
        }

        mediaPath = args[0];
        frameNumber = Integer.parseInt(args[1]);

        launch(args);
    }
}
